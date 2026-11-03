import sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from download_polymarket_history import windows, classify, event_pages, history
from polymarket_backtest import mapping, align, evaluate_signals, scores


def market(**kw):
    d=dict(cycle=2024,market_id='1',question='Will the Democrats win the Texas Senate election in 2024?',
           category='winner',description='The general election is November 5, 2024.',outcome_first='Yes',outcome_second='No',payout_first=0.,exclusion_reason='')
    d.update(kw);return d


def inputs():
    m=pd.DataFrame([market()]);p=pd.DataFrame([dict(market_id='1',timestamp=pd.Timestamp(t,tz='UTC'),price_first=v) for t,v in [('2024-10-31 20:00',.2),('2024-11-01 01:00',.3)]])
    f=pd.DataFrame([dict(cycle=2024,geography='TX',scenario='oct31',target_id='2024-TX-regular-gen',model='Bayesian',model_code='GB',forecast_date=pd.Timestamp('2024-10-31',tz='UTC'),available_at=pd.Timestamp('2024-11-01',tz='UTC'),p_dem=.4,actual=-.1,provenance='test')])
    c=pd.DataFrame([dict(market_id='1',status='available')]);return m,p,f,c


def test_bounded_windows():
    w=list(windows('2024-01-01T00:00Z','2024-11-05T00:00Z'))
    assert all(0<b-a<=14*86400 for a,b in w)
    assert all(w[i][1]==w[i+1][0] for i in range(len(w)-1))
    assert w[-1][1]==pd.Timestamp('2024-11-05',tz='UTC').timestamp()


def test_short_pages_do_not_terminate_discovery():
    class API:
        def get(self,url,params):
            return [{'id':str(params['offset'])}] if params['offset']<2 else []
    assert len(list(event_pages(API(),2024)))==26


def test_scope_excludes_house_and_primaries():
    assert classify({'title':'2024 Senate elections'},{'question':'Will Democrats win the House and Senate in 2024?'},2024)[0]=='excluded'
    assert classify({'title':'2022 Senate'},{'question':'Who wins the Senate primary in 2022?'},2022)[0]=='excluded'
    assert classify({'title':'2024 Senate'},{'question':'How many Republican Senate seats after 2024?'},2024)[0]=='seats'


def test_outcome_mapping_and_independents():
    assert mapping(SimpleNamespace(**market(outcome_first='Republicans',outcome_second='Democrats')))[1]=='R'
    assert mapping(SimpleNamespace(**market(outcome_first='No',outcome_second='Yes')))[1]=='R'
    assert mapping(SimpleNamespace(**market(question='Will Democrats win the Maine Senate election in 2024?')))[1]==''
    assert mapping(SimpleNamespace(**market(question='Will Bob win the Texas Senate election in 2024?')))[1]==''


def test_alignment_never_uses_price_before_forecast():
    q,a=align(*inputs());assert len(q)==1;assert q.price_first.iloc[0]==.3
    assert q.settlement_verified.iloc[0]
    m,p,f,c=inputs();c['status']='partial';assert align(m,p,f,c)[0].empty
    m,p,f,c=inputs();p['timestamp']+=pd.Timedelta(days=4);assert align(m,p,f,c)[0].empty


def test_settlement_disagreement_blocks_profit():
    m,p,f,c=inputs();m['payout_first']=1.;q,_=align(m,p,f,c)
    assert not q.settlement_verified.iloc[0]
    sig=pd.DataFrame([dict(cycle=2024,scenario='oct31',market_id='1',model_code='GB',side='first',shares=100)])
    with unittest.TestCase().assertRaises(ValueError):evaluate_signals(q,sig)
    assert scores(q).empty


def test_profit_sides_cost_and_friction():
    q,_=align(*inputs());sig=pd.DataFrame([dict(cycle=2024,scenario='oct31',market_id='1',model_code='GB',side=s,shares=100) for s in ['first','second']])
    trades=evaluate_signals(q,sig,friction_cents=1.)
    np.testing.assert_allclose(trades.cost,[31,71]);np.testing.assert_allclose(trades.realized_profit,[-31,29])
    np.testing.assert_allclose(trades.expected_profit,[9,-11])
    with unittest.TestCase().assertRaises(ValueError):evaluate_signals(q,sig.assign(shares=-1))
    with unittest.TestCase().assertRaises(ValueError):evaluate_signals(q,pd.concat([sig,sig]))


def test_scores_do_not_double_count_complementary_markets():
    q,_=align(*inputs());other=q.copy();other['market_id']='2'
    assert scores(pd.concat([q,other])).races.iloc[0]==1


def test_history_distinguishes_legacy_and_post_election():
    class API:
        def get(self, url, params):return {'history':[]}
    row=SimpleNamespace(category='winner',token='1',market_id='1',cycle=2022,
        start='2022-10-01T00:00Z',stop='2022-10-08T00:00Z',legacy_amm=True)
    points,status=history(API(),row)
    assert not points and status['status']=='legacy_amm_history_required'
    row.start='2022-11-09T00:00Z';row.stop='2022-11-08T00:00Z'
    points,status=history(API(),row)
    assert status['status']=='opened_after_cutoff' and status['requests']==0


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(unittest.FunctionTestCase(value) for name,value in globals().copy().items() if name.startswith("test_") and callable(value))

if __name__ == "__main__":
    unittest.main()
