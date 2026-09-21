#!/usr/bin/env python3
"""Build fixed feature scores from the latest verified bundle, without model fits.

Usage: python scripts/summarize_features.py [--snapshot PATH] [--output PATH]
Refresh source data separately with refresh_2026.py; this command never downloads.
"""
import argparse
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,shutil
import pandas as pd
from load_final_dataset import open_dataset
from contextual_baselines import make_store,calendar_inputs
from feature_scores import build_score_panel,MODEL_COLUMNS,CONFIG_PATH


def save_scores(data,calendars,output,endpoint_ledger=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    scores,components,normalizers=build_score_panel(calendars)
    current=scores[scores.cycle.eq(pd.Timestamp(data.policy['as_of']).year)&scores.scenario.eq('matched_live')]
    for name,frame in [('scores',scores),('components',components),('source_calendars',calendars),('current_scores',current)]:
        frame.to_parquet(output/(name+'.parquet'),index=False)
    if endpoint_ledger is not None:endpoint_ledger.to_parquet(output/'endpoint_ledger.parquet',index=False)
    (output/'normalizers.json').write_text(json.dumps(normalizers,indent=2,allow_nan=False)+'\n')
    settings=dict(version=json.loads(CONFIG_PATH.read_text())['version'],model_columns=MODEL_COLUMNS,
        role='feature summarizer only; no new predictions or fitted electoral coefficients',
        diagnostic_panel='each row uses only earlier cycles in the same calendar for normalization',
        future_model_use='refit transformer inside each inner/outer training fold; same normalizer for training and held-out rows',
        party_orientation='WH sign on economic/public opinion scores; disruption unsigned binary',
        missingness='strict complete ingredients; no neutral-zero imputation',
        data_view='reference; latest-revised source and availability limits inherited',
        extra_event_window='existing OR, Jan of Y-4 through last eligible closed month; not literal48months')
    data.write_run_metadata(output/'data_inputs.json',feature_view='reference',tables=['contest_inputs_reference'],run_config=settings)
    (output/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    shutil.copy2(CONFIG_PATH,output/CONFIG_PATH.name)
    for name in ['feature_scores.py','summarize_features.py','alignment_features.py','contextual_baselines.py','disruption_features.py']:
        shutil.copy2(Path(__file__).parent/name,output/name)
    (output/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(output.iterdir()) if p.is_file()},indent=2)+'\n')
    return scores,components,normalizers,current


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();data=open_dataset(args.snapshot)
    store=make_store(data);panels=[];endpoints=[]
    for scenario in ['matched_live','oct31']:
        _,panel,ledger=calendar_inputs(data,store,scenario);panels.append(panel);endpoints.append(ledger)
    out=args.output or Path(__file__).resolve().parents[1]/'reports/feature_scores'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    _,_,_,current=save_scores(data,pd.concat(panels,ignore_index=True),out,pd.concat(endpoints,ignore_index=True))
    print('Saved:',out)
    print(current[['cycle','context_id']+MODEL_COLUMNS+['model_inputs_complete']].to_string(index=False))


if __name__=='__main__':main()
