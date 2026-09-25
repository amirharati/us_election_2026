"""One-time upgrade of an older saved live forecast, using its exact saved inputs.

No downloads or historical training. Future notebook04 runs save draws directly.
"""
from pathlib import Path
import sys,json,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
import pandas as pd
from pandas.testing import assert_frame_equal


def upgrade(run):
    run=lab.verify_run(Path(run));meta=json.loads((run/'run.json').read_text())
    from model_portfolio import configuration
    if meta['ensemble']!=configuration():raise ValueError('Saved mixture configuration differs; cannot reproduce this forecast')
    snapshot=lab.dataset_for_run(meta)
    rebuilt=lab.live_forecast(snapshot,as_of=meta['as_of'],feature_mode=meta.get('feature_mode','dated'),
        weights=meta['weights'],freshness=meta.get('freshness'),output_kind='distribution_rebuild')
    for name in ['predictions','seats']:
        old=pd.read_parquet(run/(name+'.parquet'));new=pd.read_parquet(rebuilt/(name+'.parquet'))
        assert_frame_equal(old,new,check_exact=False,atol=1e-10,rtol=1e-10)
    out=lab.new_run('live');shutil.copytree(run,out,dirs_exist_ok=True)
    for path in [rebuilt/'main_joint.npz',*(rebuilt/'model_forecasts').glob('*.npz')]:
        shutil.copy2(path,out/path.relative_to(rebuilt))
    meta['predictive_export']={'version':1,'source_manifest_sha256':lab.sha(run/'manifest.json'),
        'note':'Reproduced exact saved evidence and verified unchanged predictions/seats; retained full component simulations.'}
    lab.finish(out,meta,publish=False);lab.verify_run(out);lab.publish_run(out)
    return out


if __name__=='__main__':
    print(upgrade(Path(sys.argv[1]) if len(sys.argv)>1 else lab.latest_run('live')))
