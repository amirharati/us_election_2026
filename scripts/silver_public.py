"""Read only Silver Bulletin's publicly rendered text; never subscriber payloads."""
from datetime import datetime
from email.utils import parsedate_to_datetime
import hashlib
import re
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

LANDING = 'https://www.natesilver.net/p/nate-silver-2026-midterm-election-polls-model'
FEED = 'https://www.natesilver.net/feed'


def public_topline(raw, url, fallback_date=None):
    soup=BeautifulSoup(raw,'html.parser')
    body=soup.select_one('.available-content')
    if body is None:
        return None
    # Do not inspect serialized subscriber text, hidden content or the paywall.
    for node in body.select('script,style,.paywall,[hidden],[aria-hidden="true"]'):
        node.decompose()
    text=body.get_text(' ',strip=True)
    text=re.sub(r'\s+',' ',text).replace('’',"'").replace('“','"').replace('”','"')
    paragraphs=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)).replace('’',"'").replace('“','"').replace('”','"') for p in body.find_all('p')]
    values=[]
    for paragraph in paragraphs:
        if not all(word in paragraph.lower() for word in ['democrat','senate','deluxe']):
            continue
        # Deliberately narrow patterns: do not confuse a rating cutoff, a model range,
        # a polling number, or prediction-market odds with Deluxe's own probability.
        patterns=[r'including\s+(\d+(?:\.\d+)?)\s*(?:percent|%)\s+in our\s+(?:headline\s+)?["\']?Deluxe',
                  r"Democrats'?\s+chances of (?:retaking|winning|taking|controlling) the Senate\s+(?:are\s+)?(?:now\s+)?(?:up to|at)\s+(\d+(?:\.\d+)?)\s*(?:percent|%)\s+in our\s+[\"']?Deluxe"]
        for pattern in patterns:
            values.extend(float(v) for v in re.findall(pattern,paragraph,re.I))
    if len(set(values))!=1 or not 0<=values[0]<=100:
        return None
    if url==LANDING:
        date_match=re.search(r'Updated\s+([A-Z][a-z]+ \d{1,2}, 2026)',text)
        if date_match is None:return None
        date=datetime.strptime(date_match[1],'%B %d, %Y').date().isoformat()
    else:
        # RSS publication date belongs to this exact article, not the landing page.
        if fallback_date is None:return None
        date=fallback_date
    return dict(published_date=date,published_label=date,rows=[],D_control_pct=values[0],expected_D=None,
                scope='public_topline_only',source_url=url,feed_url=FEED,
                raw_sha256=hashlib.sha256(raw).hexdigest(),
                availability='Rounded Deluxe Senate-control probability from public text. State probabilities and expected seats are subscriber-only and unavailable here.')


def fetch_silver(fetch, timeout):
    observations={};candidates=[];errors=[]
    try:
        raw=fetch(LANDING,timeout);observations[LANDING]=hashlib.sha256(raw).hexdigest()
        snapshot=public_topline(raw,LANDING)
        if snapshot:candidates.append(snapshot)
    except (ValueError,OSError) as exc:
        errors.append(type(exc).__name__)
    try:
        raw=fetch(FEED,timeout);observations[FEED]=hashlib.sha256(raw).hexdigest()
        items=ET.fromstring(raw).findall('./channel/item')
        checked=0
        for item in items[:20]:
            url=item.findtext('link','');parts=urlsplit(url)
            if parts.scheme!='https' or parts.netloc!='www.natesilver.net' or not parts.path.startswith('/p/') or url==LANDING:
                continue
            # The RSS description is used for discovery only. Parse the actual public page.
            description=BeautifulSoup(item.findtext('description','')+' '+item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded',''),'html.parser').get_text(' ',strip=True)
            if not all(word in description.lower() for word in ['senate','deluxe']):continue
            date=parsedate_to_datetime(item.findtext('pubDate')).date().isoformat()
            if candidates and date<=max(s['published_date'] for s in candidates):continue
            checked+=1
            try:
                article=fetch(url,timeout);observations[url]=hashlib.sha256(article).hexdigest()
                snapshot=public_topline(article,url,date)
                if snapshot:candidates.append(snapshot)
            except (ValueError,OSError) as exc:
                errors.append(type(exc).__name__)
            if checked>=4:break
    except (ValueError,OSError,ET.ParseError,TypeError) as exc:
        errors.append(type(exc).__name__)
    if not candidates:
        raise ValueError('No unambiguous Deluxe Senate-control probability in public text; detailed tables require a subscription.'+(' Source checks: '+', '.join(errors) if errors else ''))
    result=max(candidates,key=lambda s:(s['published_date'],s['source_url']==LANDING))
    result['discovery_sha256']=observations
    result['discovery_errors']=errors
    return result
