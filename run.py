"""One command for standalone reproduction, training, acquisition and forecasting."""
import argparse
import subprocess
import sys
import election_lab as lab


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('task',choices=['reproduce','weights','train','student','live','report','download-history','scenarios','matched-student','portfolio','poll-weights','audit'])
    p.add_argument('--force',action='store_true',help='Recheck public sources even inside cache TTL')
    p.add_argument('--offline',action='store_true',help='Use verified caches with explicit offline status')
    p.add_argument('--strict',action='store_true',help='Fail rather than retain stale sources after a download failure')
    p.add_argument('--no-student',action='store_true',help='Skip slower Student MCMC for live forecasts')
    p.add_argument('--ttl-hours',type=float,default=6.)
    p.add_argument('--timeout',type=float,default=20.)
    p.add_argument('--year',type=int,default=2026)
    p.add_argument('--scenario',choices=['matched_live','oct31'],default='matched_live')
    a=p.parse_args()
    if a.task=='reproduce':out=lab.reproduce()
    elif a.task=='weights':out=lab.weight_experiment()
    elif a.task=='train':out=lab.refit_main(a.scenario,a.year)
    elif a.task=='student':
        pred,d=lab.rerun_student(a.scenario,a.year);out=lab.new_run('student_refit')
        pred.to_parquet(out/'predictions.parquet',index=False);d['diagnostics'].to_parquet(out/'diagnostics.parquet',index=False)
        out=lab.finish(out,dict(scenario=a.scenario,cycle=a.year,df=5,warmup=d['warmup'],draws=d['draws'],chains=d['chains']))
    elif a.task=='live':out=lab.refresh(force=a.force,offline=a.offline,strict=a.strict,ttl_hours=a.ttl_hours,timeout=a.timeout,include_student=not a.no_student)
    elif a.task=='report':
        from live_forecast_report import save_report
        from live_uncertainty_watchlist import build_watchlist
        import pandas as pd
        live=lab.latest_run('live')
        models=pd.read_parquet(live/'predictions.parquet').model.unique().tolist()
        out=save_report(live,build_watchlist(live,models))
    elif a.task=='matched-student':
        from matched_student import run
        out=run(force=a.force)
    elif a.task=='poll-weights':
        from poll_weight_experiment import run
        out=run(force=a.force)
    elif a.task=='portfolio':
        from model_portfolio import run
        out=run(force=a.force)
    elif a.task=='scenarios':
        from release_scenarios import run
        out=run()
    elif a.task=='download-history':
        # Raw history is independently cached. Replacing reviewed historical
        # training labels requires an explicit audit, not a live-data refresh.
        subprocess.run([sys.executable,str(lab.ROOT/'scripts/download_historical.py')],check=True);return
    else:
        from release_audit import audit
        print(audit());return
    if a.task=='live':
        from live_forecast_report import save_report
        from live_uncertainty_watchlist import build_watchlist
        import pandas as pd
        models=pd.read_parquet(out/'predictions.parquet').model.unique().tolist()
        save_report(out,build_watchlist(out,models))
    from output_publication import result_path
    print('Published results:',result_path(lab.ROOT,out.parent.name))
    print('Readable reports:',lab.ROOT/'outputs/README.md')
    print('Local execution archive:',out)


if __name__=='__main__':main()
