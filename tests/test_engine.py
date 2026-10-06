from datetime import datetime,timezone,timedelta
import sqlite3
from psychohistory.core.models import Observation,Forecast
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.validation.scoring import brier
from psychohistory.g2.ou import fit_ou
from psychohistory.g3.spectral import laplacian_metrics
from psychohistory.g23.gate import coupling_gate

def T(d): return datetime(2020,1,1,tzinfo=timezone.utc)+timedelta(days=d)
def test_asof_blocks_future(tmp_path):
 s=Store(tmp_path/'x.db'); s.add_observation(Observation('a','x',T(0),T(2),1,'src')); assert not s.observations_as_of(T(1)); assert len(s.observations_as_of(T(2)))==1
def test_forecasts_immutable(tmp_path):
 s=Store(tmp_path/'x.db'); f=Forecast('f','e',T(0),T(1),.2,'m',.3); s.add_forecast(f)
 try:s.add_forecast(f); assert False
 except sqlite3.IntegrityError:pass
def test_score_only_matured(tmp_path):
 s=Store(tmp_path/'x.db'); s.add_forecast(Forecast('f','e',T(0),T(2),.2,'m',.3)); s.resolve('e',1,T(1)); assert s.scored()==[]
def test_brier():
 r=[('f',.2,.4,0),('g',.8,.6,1)]; x=brier(r); assert abs(x['brier']-.04)<1e-9 and x['brier_skill']>0
def test_ancestry_breadth():
 o=[Observation('a','x',T(0),T(0),1,'s',ancestry=('shock',)),Observation('b','y',T(0),T(0),2,'s',ancestry=('shock',))]; v=validate_observations(o,T(1)); assert v['informational_breadth_upper_bound']==1
def test_ou_and_graph():
 x=fit_ou(range(8),[1,.8,.7,.55,.5,.42,.4,.35]); assert x['status'] in {'VALID','UNRESOLVED'}
 g=laplacian_metrics([[0,1,0],[1,0,1],[0,1,0]]); assert g['lambda2']>0
def test_g23_refuses_weak_evidence(): assert coupling_gate(out_of_sample_gain=.1)['status']=='TEST_UNRESOLVED'
