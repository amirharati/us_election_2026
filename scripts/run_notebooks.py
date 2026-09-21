"""Execute all release notebooks with the active Python and forbid legacy data reads."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
import traceback
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT=Path(__file__).resolve().parents[1]


def run(start=1):
    out=ROOT/'outputs/validation';out.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'cache/matplotlib'))
    os.environ.setdefault('NUMBA_CACHE_DIR',str(ROOT/'cache/numba'))
    os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
    guard="""import sys as _sys
from pathlib import Path as _Path
_compact_root = _Path.cwd().resolve()
def _forbid_legacy_data(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes)):
        p = _Path(args[0].decode() if isinstance(args[0], bytes) else args[0]).resolve()
        if p.is_relative_to(_compact_root/'data') and not p.is_relative_to(_compact_root/'data/compact'):
            raise RuntimeError('Notebook attempted a legacy/raw data read: '+str(p))
_sys.addaudithook(_forbid_legacy_data)
print('Verification: legacy data reads blocked; compact inputs and local download cache allowed.')
"""
    report=[]
    status=out/'notebooks.json'
    logs_dir=ROOT/'cache/notebook_execution';logs_dir.mkdir(parents=True,exist_ok=True)
    if start>1 and status.exists():report=[r for r in json.loads(status.read_text()) if int(r['notebook'][:2])<start]
    with tempfile.TemporaryDirectory(prefix='election-kernel-') as temp:
        spec=Path(temp)/'election-verify';spec.mkdir()
        (spec/'kernel.json').write_text(json.dumps(dict(argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],display_name='Election verification',language='python')))
        for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
            if int(path.name[:2])<start:continue
            begin=time.monotonic();print('RUN',path.name,flush=True)
            notebook=nbformat.read(path,as_version=4)
            notebook.cells.insert(0,nbformat.v4.new_code_cell(guard))
            manager=KernelManager(kernel_name='election-verify',kernel_spec_manager=KernelSpecManager(kernel_dirs=[temp]))
            result=dict(notebook=path.name,status='running',legacy_data_reads_blocked=True)
            try:
                NotebookClient(notebook,km=manager,timeout=7200,resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
                result['status']='passed'
            except Exception:
                result['status']='failed';result['error']=traceback.format_exc()
            finally:
                if manager.has_kernel:manager.shutdown_kernel(now=True)
                notebook.cells.pop(0)
                result['seconds']=round(time.monotonic()-begin,2)
                logs=[]
                for c in notebook.cells:
                    for o in c.get('outputs',[]):
                        if o.output_type=='stream':logs.append(o.text)
                        if o.output_type=='error':logs.append('\n'.join(o.traceback))
                (logs_dir/(path.stem+'.log')).write_text('\n'.join(logs))
                # Preserve failed executions separately; successful notebooks are saved in place.
                nbformat.write(notebook,path if result['status']=='passed' else logs_dir/path.name)
                result['notebook_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
                report.append(result);status.write_text(json.dumps(report,indent=2)+'\n')
                lines=['# Notebook execution', '', 'Executed in order with legacy raw-data reads blocked. Successful notebooks are saved in place; logs and failed attempts stay in the ignored local cache.', '',
                       '| Notebook | Status | Seconds |', '|---|---|---:|']
                lines += [f"| [{r['notebook']}](../../notebooks/{r['notebook']}) | {r['status']} | {r['seconds']:.2f} |" for r in report]
                (out/'notebooks.md').write_text('\n'.join(lines)+'\n')
                print(result['status'].upper(),path.name,result['seconds'],'seconds',flush=True)
            if result['status']=='failed':
                print(result['error'],flush=True);return 1
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',type=int,default=1)
    sys.exit(run(p.parse_args().start))
