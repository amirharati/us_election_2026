"""Publish a new aligned snapshot with reviewed official historical results.

Preserve the base snapshot's polls, features and as-of date. The same result
review also runs automatically in future accepted/final refresh builds.
"""
from pathlib import Path
import argparse
import json
from data_utils import LAB
from build_accepted_data import build,publish
from verify_accepted_data import verify
from build_final_dataset import build_final


def repair(base):
    from verify_final_dataset import verify as verify_final
    base=Path(base).resolve();verify_final(base)
    prov=json.loads((base/'provenance.json').read_text());policy=json.loads((base/'policy.json').read_text())
    config=Path(prov['accepted_snapshot'])/'config.json'
    accepted=publish(build(config),LAB/'data/final_inputs/accepted',config);verify(accepted)
    return build_final(accepted,prov['prepared_feature_snapshot'],prov['political_snapshot'],policy['as_of'],LAB/'data/final',
                       dict(parent_snapshot=str(base),change='Reviewed official historical results; original poll receipt dates retained; no polling/feature acquisition'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base-snapshot',type=Path,default=LAB/'data/final/snapshots/20260918T040848.452707Z')
    print(repair(p.parse_args().base_snapshot))
