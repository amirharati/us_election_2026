"""Automatic, attributed comparisons with public 2026 Senate forecasts and ratings."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import html
import json
import re

import pandas as pd
import requests

import election_lab as lab
from compare_current_forecasts import ABBR
from data_utils import atomic_json
from model_labels import model_label

SOURCES = {
    'silver': ('Silver Bulletin Deluxe', 'https://www.natesilver.net/p/nate-silver-2026-midterm-election-polls-model',
               'https://www.natesilver.net/feed'),
    'rttwh': ('Race to the WH', 'https://www.racetothewh.com/senate/26',
              'https://live-data.jifo.co/6911ecb8-c744-4464-a182-70568e288364'),
    'inside': ('Inside Elections', 'https://insideelections.com/ratings/senate/',
               'https://insideelections.com/wp-content/themes/inside-elections/cache/ratings_latest_senate_year=2026_district=all_clean.json'),
}
METHOD = (
    'This section is generated from publisher feeds on each live rerun. It compares the Gaussian Bayesian '
    'reference and the four-model mixture with published forecasts. A numerical mismatch means opposite '
    'favored winners or a D/Independent win probability gap of at least {gap:g} percentage points. '
    'For ratings, a mismatch means opposite favored parties, or a publisher toss-up when our model gives '
    'one party at least {conf:g}% probability. Ratings are never converted into probabilities. '
    'These are differences of opinion, not evidence that either forecast is wrong. Sources can use different '
    'data dates and methods. Chamber totals retain each publisher’s own independent-caucus convention. '
    'Independent candidates count on the D/Independent side in state comparisons. Published D and independent '
    'win probabilities are added once; independents already in a publisher’s D column are not added again. '
    'This is our comparison assumption, not a claim about their party affiliation or future caucus. '
    'Silver supplies only a dated, rounded public Deluxe topline; its detailed subscriber forecasts are unavailable. '
    'Publisher releases after our cutoff are excluded. A successful download does not mean the forecast was updated today.'
)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def number(text):
    return float(re.search(r'[-+]?\d+(?:\.\d+)?', str(text))[0])


def parse_rttwh(data):
    sheets = dict(zip(data['sheetNames'], data['data']))
    # Use named sheets and explicit headers so a rearranged workbook cannot silently change meanings.
    win = sheets['Win']
    if win[0][:4] != ['', 'D', 'R', 'Ind']:
        raise ValueError('Unrecognized publisher probability columns')
    rows = []
    for row in win[1:]:
        if row[0] not in ABBR:
            continue
        values = [number(v.rsplit(':', 1)[1]) if v else 0. for v in row[1:4]]
        if len(values) != 3 or any(not 0 <= v <= 100 for v in values) or abs(sum(values)-100) > .3:
            raise ValueError('Publisher probabilities do not sum to 100')
        rows.append(dict(geography=ABBR[row[0]], seat_class=None, p_dem=values[0]/100,
                         independent_pct=values[2], rating=None, rating_date=None))
    update = sheets['Last Update'][0][0]
    match = re.search(r'([A-Z][a-z]{2}) (\d{1,2}),', update)
    if not match:
        raise ValueError('Missing publisher forecast date')
    # This adapter is explicitly for the 2026 forecast; retrieval time is not its publication date.
    date = datetime.strptime('2026 '+match[1]+' '+match[2], '%Y %b %d').date().isoformat()
    control, seats = sheets['Chance to Win'], sheets['Projected Seats']
    if control[0][1:3] != ['Democrats', 'Republicans'] or seats[0][1:3] != ['Democrats', 'Republicans']:
        raise ValueError('Unrecognized chamber columns')
    return dict(published_date=date, published_label=update, rows=rows,
                D_control_pct=number(control[1][1]), expected_D=number(seats[1][1]))


def parse_inside(data):
    if data['office'] != 'Senate' or data['total'] != 100:
        raise ValueError('Not a full Senate ratings feed')
    rows = []
    for row in data['ratings']:
        if row['rating'] == 'Not Up This Cycle':
            continue
        if str(row['election_year']) != '2026':
            raise ValueError('Unexpected ratings cycle')
        rating = row['rating']
        if rating != 'Toss-up' and not re.fullmatch(r'(Solid|Likely|Lean|Tilt) (Democrat|Republican|Independent)', rating):
            raise ValueError('Unrecognized race rating: '+rating)
        rows.append(dict(geography=row['state'].upper(), seat_class={'I':1,'II':2,'III':3}[row['office']],
                         p_dem=None, independent_pct=None, rating=rating, rating_date=row['date'][:10]))
    return dict(published_date=data['last_updated'][:10], published_label=data['last_updated'], rows=rows,
                D_control_pct=None, expected_D=None)


PARSERS = {'rttwh': parse_rttwh, 'inside': parse_inside}


def validate(snapshot):
    pd.Timestamp(snapshot['published_date'])
    rows = snapshot['rows']
    public_topline = snapshot.get('scope') == 'public_topline_only'
    if public_topline and (rows or snapshot['D_control_pct'] is None):
        raise ValueError('Invalid public topline-only snapshot')
    if not public_topline and not 30 <= len(rows) <= 40:
        raise ValueError('Incomplete or unexpected number of Senate contests')
    keys = [(r['geography'], r['seat_class']) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate publisher contests')
    for r in rows:
        if r['geography'] not in ABBR.values():
            raise ValueError('Unknown state')
        if r['p_dem'] is not None:
            independent = r['independent_pct'] or 0
            if not 0 <= r['p_dem'] <= 1 or not 0 <= independent <= 100 or r['p_dem'] + independent/100 > 1.003:
                raise ValueError('Invalid party or combined D/Independent probability')
    for key, upper in [('D_control_pct',100),('expected_D',100)]:
        if snapshot[key] is not None and not 0 <= snapshot[key] <= upper:
            raise ValueError('Invalid chamber value')
    return snapshot


def download(url, timeout):
    with requests.get(url, timeout=timeout, stream=True) as response:
        response.raise_for_status()
        chunks=[];size=0
        for chunk in response.iter_content(65536):
            size += len(chunk)
            if size > 2_000_000:
                raise ValueError('Publisher feed exceeds 2 MB')
            chunks.append(chunk)
        return b''.join(chunks)


def cached_snapshot(key):
    path = lab.ROOT/'cache/published_forecasts'/f'{key}.json'
    candidates = [path]
    # Portable, normalized fallback for a clone without a local download cache.
    published = lab.ROOT/'outputs/reports/forecast'
    if (published/'published_sources.json').exists():
        try:
            lab.verify_run(published)
            saved=json.loads((published/'published_sources.json').read_text())
        except (ValueError, OSError, KeyError):
            saved={}
    else:
        saved={}
    for candidate in candidates:
        try:
            wrapped=json.loads(candidate.read_text())
            if wrapped['sha256'] != digest(wrapped['snapshot']):
                raise ValueError('Publisher cache checksum failed')
            return validate(wrapped['snapshot'])
        except (ValueError, OSError, KeyError, TypeError):
            continue
    if key in saved:
        return validate(saved[key])
    return None


def acquire(key, *, offline=False, force=False, ttl_hours=6, timeout=20):
    old=cached_snapshot(key);now=datetime.now(timezone.utc)
    status=dict(Source=SOURCES[key][0], URL=SOURCES[key][1], Status='unavailable',
                Published=None, Retrieved=None, Error='')
    snapshot=None
    if offline:
        snapshot=old;status['Status']='offline_cache' if old else 'unavailable_offline'
    elif old and not force and 0 <= (now-pd.Timestamp(old['retrieved_at'])).total_seconds() < ttl_hours*3600:
        snapshot=old;status['Status']='fresh_check_cache'
    else:
        try:
            if key == 'silver':
                from silver_public import fetch_silver
                snapshot=validate(fetch_silver(download, timeout))
            else:
                raw=download(SOURCES[key][2], timeout)
                snapshot=validate(PARSERS[key](json.loads(raw)))
                snapshot.update(source_url=SOURCES[key][1],feed_url=SOURCES[key][2],raw_sha256=hashlib.sha256(raw).hexdigest())
            snapshot['retrieved_at']=now.isoformat()
            path=lab.ROOT/'cache/published_forecasts'/f'{key}.json'
            path.parent.mkdir(parents=True,exist_ok=True)
            atomic_json(path,dict(snapshot=snapshot,sha256=digest(snapshot)))
            status['Status']='checked_online'
        except (requests.RequestException, ValueError, KeyError, TypeError, IndexError, OSError) as exc:
            snapshot=old;status['Status']='stale_cache_after_failure' if old else 'unavailable'
            status['Error']=f'{type(exc).__name__}: {str(exc)[:250]}'
    if snapshot:
        status.update(Published=snapshot['published_date'], Retrieved=snapshot['retrieved_at'],
                      URL=snapshot.get('source_url',SOURCES[key][1]),
                      Coverage=snapshot.get('availability','Public race ratings' if key=='inside' else 'State and chamber forecasts'))
    return snapshot,status


def favored(prob):
    return 'D' if prob > .5 else 'R' if prob < .5 else 'Tie'


def compare(predictions, seats, snapshots, cutoff, independent_states, models, gap_pp, confidence):
    overall=[];states=[];excluded=[];ratings=[];chamber_gaps=[]
    for model in models:
        seat=seats[seats.model.eq(model)]
        if seat.empty:continue
        s=seat.iloc[0]
        overall.append({'Forecast':model_label(model),'Date':cutoff,'D control %':100*s.p_D_control,
                        'Expected D seats':s.expected_D,'Coverage':'Our model'})
    for key,snapshot in snapshots.items():
        if snapshot['published_date'] > cutoff:
            excluded.append(dict(Source=SOURCES[key][0],Contest='All',Reason='Publisher release is later than our forecast cutoff.'))
            continue
        if snapshot['D_control_pct'] is not None:
            for row in overall[:len([m for m in models if m in seats.model.values])]:
                gap=row['D control %']-snapshot['D_control_pct']
                chamber_gaps.append({'Model':row['Forecast'],'Publisher':SOURCES[key][0],
                    'Published':snapshot['published_date'],'Our D control %':row['D control %'],
                    'Published D control %':snapshot['D_control_pct'],'Gap (pp)':gap,
                    'Expected-seat gap':row['Expected D seats']-snapshot['expected_D'] if snapshot['expected_D'] is not None else None,
                    'Comparison':'The models favor different Senate majorities.' if favored(row['D control %']/100)!=favored(snapshot['D_control_pct']/100) else 'The models favor the same Senate majority.'})
            overall.append({'Forecast':SOURCES[key][0],'Date':snapshot['published_date'],
                            'D control %':snapshot['D_control_pct'],'Expected D seats':snapshot['expected_D'],
                            'Coverage':snapshot.get('availability','Published forecast.')})
        for model in models:
            local=predictions[predictions.model.eq(model)]
            matched_rating=[]
            for external in snapshot['rows']:
                state=external['geography'];part=local[local.geography.eq(state)]
                reason=None
                if len(part)!=1:
                    reason='No unique local contest matches this state.'
                elif external['seat_class'] is not None and int(part.iloc[0].target_id.split('-')[2])!=external['seat_class']:
                    reason='Senate seat classes differ.'
                if reason:
                    if model==models[0]:excluded.append(dict(Source=SOURCES[key][0],Contest=state,Reason=reason))
                    continue
                row=part.iloc[0];ours=float(row.p_dem);party=favored(ours)
                contest=state+(' (special)' if row.special else '')
                gap=None;selection='';rating=external['rating'];prob=external['p_dem']
                mapping = 'Independents count with D for this comparison.' if state in independent_states or (external['independent_pct'] or 0)>0 or 'Independent' in (rating or '') else 'D versus R.'
                if prob is not None:
                    # Publisher columns are mutually exclusive. D may already contain an independent.
                    prob = min(1., prob + (external['independent_pct'] or 0)/100)
                    gap=100*(ours-prob)
                    if party!=favored(prob) and party!='Tie' and favored(prob)!='Tie':
                        selection='The forecasts favor different parties.'
                    if abs(gap)>=gap_pp:
                        selection+=' '+f'Our D/Independent win probability is {abs(gap):.1f} points '+('higher.' if gap>0 else 'lower.')
                else:
                    other='D' if ('Democrat' in rating or 'Independent' in rating) else 'R' if 'Republican' in rating else 'Toss-up'
                    matched_rating.append((party,other))
                    if other!='Toss-up' and party not in (other,'Tie'):
                        selection='Our favored party differs from the published rating.'
                    elif other=='Toss-up' and max(ours,1-ours)>=confidence:
                        selection=f'The publisher rates this a toss-up. Our model gives {party} {100*max(ours,1-ours):.1f}%.'
                states.append({'Source':SOURCES[key][0],'Published':snapshot['published_date'],
                    'Model':model_label(model),'Contest':contest,'Our D/Independent win %':100*ours,
                    'Published D/Independent win %':100*prob if prob is not None else None,'Published rating':rating,
                    'Gap (pp)':gap,'Side definition':mapping,'Reason':selection.strip(),'selected':bool(selection.strip())})
            if matched_rating:
                ratings.append({'Model':model_label(model),'Matched races':len(matched_rating),
                    'Our D/Independent favored':sum(a=='D' for a,b in matched_rating),'Our R favored':sum(a=='R' for a,b in matched_rating),
                    'Publisher D/Independent favored':sum(b=='D' for a,b in matched_rating),
                    'Publisher R favored':sum(b=='R' for a,b in matched_rating),
                    'Publisher toss-ups':sum(b=='Toss-up' for a,b in matched_rating)})
    state_columns=['Source','Published','Model','Contest','Our D/Independent win %','Published D/Independent win %','Published rating','Gap (pp)','Side definition','Reason','selected']
    all_states=pd.DataFrame(states,columns=state_columns)
    selected=all_states[all_states.selected.eq(True)].copy()
    selected=selected.assign(_gap=pd.to_numeric(selected['Gap (pp)'], errors='coerce').abs()).sort_values(['Source','Model','_gap','Contest'],ascending=[True,True,False,True]).drop(columns=['_gap','selected'])
    return dict(overall=pd.DataFrame(overall), chamber_gaps=pd.DataFrame(chamber_gaps), mismatches=selected, all_states=all_states,
                ratings=pd.DataFrame(ratings), exclusions=pd.DataFrame(excluded,columns=['Source','Contest','Reason']))


def build_published_comparison(run, *, offline=False, force=False, ttl_hours=6, timeout=20,
                               gap_pp=15, confidence=.75, models=('Bayesian','Four-model mixture')):
    if not 0<=gap_pp<=100 or not .5<confidence<=1:
        raise ValueError('Invalid comparison thresholds')
    run=lab.verify_run(run);meta=json.loads((run/'run.json').read_text())
    snapshots={};statuses=[]
    for key in SOURCES:
        snapshot,status=acquire(key,offline=offline,force=force,ttl_hours=ttl_hours,timeout=timeout)
        if snapshot:snapshots[key]=snapshot
        status['Days before our cutoff'] = (pd.Timestamp(meta['as_of'])-pd.Timestamp(snapshot['published_date'])).days if snapshot else None
        if snapshot and snapshot['published_date'] > meta['as_of']:
            status['Status'] += '; excluded_after_cutoff'
        statuses.append(status)
    roster=json.loads((lab.ROOT/'config/candidate_review_2026.json').read_text())['contests']
    independent={state for state,race in roster.items() if any(c['party'] not in ('DEM','REP') for c in race.get('candidates',[]))}
    result=compare(pd.read_parquet(run/'predictions.parquet'),pd.read_parquet(run/'seats.parquet'),
                   snapshots,meta['as_of'],independent,models,gap_pp,confidence)
    result.update(sources=snapshots,status=pd.DataFrame(statuses),parameters=dict(
        source_manifest_sha256=lab.sha(run/'manifest.json'),
        comparison_code_sha256=lab.sha(Path(__file__)),
        candidate_review_sha256=lab.sha(lab.ROOT/'config/candidate_review_2026.json'),cutoff=meta['as_of'],models=list(models),
        gap_pp=gap_pp,confidence=confidence,independent_states=sorted(independent),
        independent_policy='D_plus_independent_combined_side; no double counting of publisher D column'))
    return result


def sections(comparison):
    return [('Source dates and availability',comparison['status']),
            ('Senate control and expected seats',comparison['overall']),
            ('Chamber differences: ours minus publisher',comparison['chamber_gaps']),
            ('Inside Elections: favored-party counts in matched races',comparison['ratings']),
            ('State mismatches',comparison['mismatches']),('Excluded comparisons',comparison['exclusions'])]


def method(comparison):
    p=comparison['parameters']
    return METHOD.format(gap=p['gap_pp'],conf=100*p['confidence'])


def render_comparison(comparison):
    from IPython.display import HTML
    parts=['<p>'+html.escape(method(comparison))+'</p>']
    for title,frame in sections(comparison):
        parts.append('<h3>'+html.escape(title)+'</h3>')
        parts.append(frame.to_html(index=False,escape=True,render_links=True,na_rep='—',float_format=lambda v:f'{v:.1f}') if not frame.empty else '<p>No rows qualify or the source is unavailable. Check source status above.</p>')
    return HTML('<div style="overflow-x:auto;white-space:normal">'+''.join(parts)+'</div>')


def save_comparison(comparison, out):
    for key in ['overall','chamber_gaps','mismatches','all_states','ratings','exclusions','status']:
        comparison[key].to_parquet(out/f'published_{key}.parquet',index=False)
    lab.write_json(out/'published_sources.json',comparison['sources'])
    lab.write_json(out/'published_parameters.json',comparison['parameters'])
