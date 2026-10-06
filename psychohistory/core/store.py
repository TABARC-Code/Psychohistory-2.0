import json, sqlite3
from datetime import datetime
from pathlib import Path
from .models import Observation, Forecast

SCHEMA='''CREATE TABLE IF NOT EXISTS observations(observation_id TEXT PRIMARY KEY, series TEXT, effective_at TEXT, available_at TEXT, value REAL, source TEXT, vintage TEXT, revision_type TEXT, quality REAL, pipeline_position TEXT, ancestry TEXT);
CREATE TABLE IF NOT EXISTS forecasts(forecast_id TEXT PRIMARY KEY,event_id TEXT,origin TEXT,horizon_end TEXT,probability REAL,model TEXT,baseline_probability REAL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS outcomes(event_id TEXT, resolved_at TEXT, outcome INTEGER CHECK(outcome IN(0,1)), vintage TEXT, PRIMARY KEY(event_id,vintage));
CREATE TABLE IF NOT EXISTS hypotheses(hypothesis_id TEXT PRIMARY KEY,family TEXT,status TEXT,predictive_input INTEGER DEFAULT 0,metadata TEXT);'''
class Store:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(self.path); self.db.executescript(SCHEMA)
    def add_observation(self,o:Observation):
        self.db.execute('INSERT INTO observations VALUES(?,?,?,?,?,?,?,?,?,?,?)',(o.observation_id,o.series,o.effective_at.isoformat(),o.available_at.isoformat(),o.value,o.source,o.vintage,o.revision_type,o.quality,o.pipeline_position,json.dumps(o.ancestry))); self.db.commit()
    def observations_as_of(self,as_of:datetime,series=None):
        q='SELECT observation_id,series,effective_at,available_at,value,source,vintage,revision_type,quality,pipeline_position,ancestry FROM observations WHERE available_at<=?'; a=[as_of.isoformat()]
        if series: q+=' AND series=?'; a.append(series)
        q+=' ORDER BY effective_at,available_at'
        return [Observation(r[0],r[1],datetime.fromisoformat(r[2]),datetime.fromisoformat(r[3]),r[4],r[5],r[6],r[7],r[8],r[9],tuple(json.loads(r[10]))) for r in self.db.execute(q,a)]
    def add_forecast(self,f:Forecast):
        if not 0<=f.probability<=1: raise ValueError('probability must be in [0,1]')
        self.db.execute('INSERT INTO forecasts(forecast_id,event_id,origin,horizon_end,probability,model,baseline_probability) VALUES(?,?,?,?,?,?,?)',(f.forecast_id,f.event_id,f.origin.isoformat(),f.horizon_end.isoformat(),f.probability,f.model,f.baseline_probability)); self.db.commit()
    def resolve(self,event_id,outcome,resolved_at,vintage='first_release'):
        self.db.execute('INSERT INTO outcomes VALUES(?,?,?,?)',(event_id,resolved_at.isoformat(),int(outcome),vintage)); self.db.commit()
    def scored(self):
        return list(self.db.execute('SELECT f.forecast_id,f.probability,f.baseline_probability,o.outcome FROM forecasts f JOIN outcomes o ON f.event_id=o.event_id WHERE o.resolved_at>=f.horizon_end'))
