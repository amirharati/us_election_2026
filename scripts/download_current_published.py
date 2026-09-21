"""Download public2026forecast snapshots into a new dated archive."""
from pathlib import Path
from datetime import datetime,timezone
import requests,json,hashlib,concurrent.futures
from bs4 import BeautifulSoup

def download(root):
    out=Path(root)/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');(out/'raw').mkdir(parents=True);records=[]
    def get(item):
     name,url=item;r=requests.get(url,timeout=35,headers={'User-Agent':'Mozilla/5.0 election research; public data archive'});p=out/'raw'/name;p.write_bytes(r.content);record=dict(file=name,url=url,final_url=r.url,status=r.status_code,retrieved_at=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content));return record
    items=[('rttwh.html','https://www.racetothewh.com/senate/26'),('rttwh_embed.html','https://e.infogram.com/_/vs9b6iAeARko8cuwH51x?embed_type=responsive_iframe&src=embed'),('rttwh_live.json','https://live-data.jifo.co/6911ecb8-c744-4464-a182-70568e288364'),('ddhq.html','https://votes.decisiondeskhq.com/forecast/2026/senate'),('silver.html','https://www.natesilver.net/p/nate-silver-2026-midterm-election-polls-model')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
     for r in pool.map(get,items):records.append(r);print(r['file'],r['status'],r['bytes'],flush=True)
    soup=BeautifulSoup((out/'raw/ddhq.html').read_text(),'html.parser');links=sorted(set(a['href'] for a in soup.select('a[href]') if '/races/2026-11-03/' in a['href'] and a['href'].endswith('/forecast')))
    items=[('ddhq_'+u.split('/')[-2]+'.html','https://votes.decisiondeskhq.com'+u if u.startswith('/') else u) for u in links]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
     for r in pool.map(get,items):records.append(r);print(r['file'],r['status'],r['bytes'],flush=True)
    (out/'raw/download_log.json').write_text(json.dumps(records,indent=2)+'\n');print('OUTPUT',out)
    return out.resolve()

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]/"reports/current_published_scenarios");a=p.parse_args();print(download(a.root))
