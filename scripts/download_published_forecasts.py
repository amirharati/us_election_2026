"""Download public, historical forecast files; retain source and response provenance."""
from pathlib import Path
from datetime import datetime,timezone
import requests,json,hashlib
ROOT=Path(__file__).resolve().parents[1]/'reports/published_forecasts/raw'
URLS={'rttwh_final_embed2.html': 'https://e.infogram.com/_/xG5BaIEpiXqNRS2dysz6?src=embed', '538_2022_archive_late.csv': 'https://web.archive.org/web/20250306125236id_/https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv', '538_2022_national_archive.csv': 'https://web.archive.org/web/20250306125235id_/https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_national_toplines_2022.csv', '538_2022_distribution_archive.csv': 'https://web.archive.org/web/20250306125236id_/https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_seat_distribution_2022.csv', '538_2020_national_archive.csv': 'https://web.archive.org/web/20230427025532id_/https://projects.fivethirtyeight.com/2020-general-data/senate_national_toplines_2020.csv', '538_2018_state_archive.csv': 'https://web.archive.org/web/20190907152355id_/https://projects.fivethirtyeight.com/congress-model-2018/senate_seat_forecast.csv', '538_2018_national_archive.csv': 'https://web.archive.org/web/20190907152350id_/https://projects.fivethirtyeight.com/congress-model-2018/senate_national_forecast.csv', 'economist_2022_ga.csv': 'https://raw.githubusercontent.com/TheEconomist/us-midterms-2022-change-data/main/data/ga_senate_old_v_new.csv', 'economist_2022_nv.csv': 'https://raw.githubusercontent.com/TheEconomist/us-midterms-2022-change-data/main/data/nv_senate_old_v_new.csv', 'economist_2022_pa.csv': 'https://raw.githubusercontent.com/TheEconomist/us-midterms-2022-change-data/main/data/pa_senate_old_v_new.csv', 'economist_2022_national.csv': 'https://raw.githubusercontent.com/TheEconomist/us-midterms-2022-change-data/main/data/senate_toplines_old_v_new.csv', '538_2020_distribution_archive.csv': 'https://web.archive.org/web/20230427025534id_/https://projects.fivethirtyeight.com/2020-general-data/senate_seat_distribution.csv', 'rttwh_2024_hub.json': 'https://live-data.jifo.co/c327a873-c27c-403b-b1ea-f2c572aa8260', 'rttwh_2024_trend.json': 'https://live-data.jifo.co/a5b574eb-6085-4eff-90d6-6cf9a2aa0fee', 'rttwh_2024_national_trend.json': 'https://live-data.jifo.co/b9c7ca59-9a4e-4cf0-bbe9-746167a1a821', '538_2020_archive.csv': 'https://web.archive.org/web/20230427025535id_/https://projects.fivethirtyeight.com/2020-general-data/senate_state_toplines_2020.csv', 'economist_2022_az.csv': 'https://raw.githubusercontent.com/TheEconomist/us-midterms-2022-change-data/main/data/az_senate_old_v_new.csv'}

def main():
 ROOT.mkdir(parents=True,exist_ok=True);rows=[]
 for name,url in URLS.items():
  if (ROOT/name).exists():
   print(name,'cached; existing snapshot preserved',flush=True);continue
  try:
   r=requests.get(url,timeout=45);row=dict(file=name,url=url,final_url=r.url,status=r.status_code,bytes=len(r.content),content_type=r.headers.get('content-type'),retrieved_at=datetime.now(timezone.utc).isoformat())
   r.raise_for_status()
   if name.endswith('.csv') and ('<html' in r.text[:1000].lower() or 'forecast' not in r.text[:1000].lower() and 'date,' not in r.text[:200].lower()):raise ValueError('Response is not a forecast CSV')
   (ROOT/name).write_bytes(r.content);row['sha256']=hashlib.sha256(r.content).hexdigest();print(name,r.status_code,len(r.content),r.url,flush=True)
  except Exception as e:row=dict(file=name,url=url,error=str(e));print(name,'ERROR',str(e)[:150],flush=True)
  rows.append(row)
 (ROOT/('retrieval_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.json')).write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
