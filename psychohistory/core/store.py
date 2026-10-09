import json
import sqlite3
from datetime import datetime, timezone
import math
from pathlib import Path

from .models import Forecast, Observation

SCHEMA = """CREATE TABLE IF NOT EXISTS observations(
observation_id TEXT PRIMARY KEY, series TEXT, effective_at TEXT, available_at TEXT,
value REAL, source TEXT, vintage TEXT, revision_type TEXT, quality REAL,
pipeline_position TEXT, ancestry TEXT, evidence_role TEXT DEFAULT 'measurement',
content_ancestry TEXT DEFAULT '[]', carrier TEXT, actor_id TEXT, community_id TEXT,
semantic_variant TEXT);
CREATE TABLE IF NOT EXISTS forecasts(forecast_id TEXT PRIMARY KEY,event_id TEXT,origin TEXT,horizon_end TEXT,probability REAL,model TEXT,baseline_probability REAL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS outcomes(event_id TEXT, resolved_at TEXT, outcome INTEGER CHECK(outcome IN(0,1)), vintage TEXT, PRIMARY KEY(event_id,vintage));
CREATE TABLE IF NOT EXISTS hypotheses(hypothesis_id TEXT PRIMARY KEY,family TEXT,status TEXT,predictive_input INTEGER DEFAULT 0,metadata TEXT);"""


def _instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timezone-aware datetime required")
    return value.astimezone(timezone.utc)

def _probability(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{label} must be a finite probability in [0,1]")

class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.executescript(SCHEMA)
        existing = {r[1] for r in self.db.execute("PRAGMA table_info(observations)")}
        migrations = {
            "evidence_role": "TEXT DEFAULT 'measurement'",
            "content_ancestry": "TEXT DEFAULT '[]'",
            "carrier": "TEXT",
            "actor_id": "TEXT",
            "community_id": "TEXT",
            "semantic_variant": "TEXT",
        }
        for name, definition in migrations.items():
            if name not in existing:
                self.db.execute(f"ALTER TABLE observations ADD COLUMN {name} {definition}")
        self.db.commit()

    def add_observation(self, o: Observation):
        self.db.execute(
            """INSERT INTO observations(
            observation_id,series,effective_at,available_at,value,source,vintage,
            revision_type,quality,pipeline_position,ancestry,evidence_role,
            content_ancestry,carrier,actor_id,community_id,semantic_variant)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                o.observation_id, o.series, _instant(o.effective_at).isoformat(),
                _instant(o.available_at).isoformat(), o.value, o.source, o.vintage,
                o.revision_type, o.quality, o.pipeline_position,
                json.dumps(o.ancestry), o.evidence_role,
                json.dumps(o.content_ancestry), o.carrier, o.actor_id,
                o.community_id, o.semantic_variant,
            ),
        )
        self.db.commit()

    def observations_as_of(self, as_of: datetime, series=None):
        q = """SELECT observation_id,series,effective_at,available_at,value,source,
        vintage,revision_type,quality,pipeline_position,ancestry,evidence_role,
        content_ancestry,carrier,actor_id,community_id,semantic_variant
        FROM observations WHERE available_at<=?"""
        args = [_instant(as_of).isoformat()]
        if series:
            q += " AND series=?"
            args.append(series)
        q += " ORDER BY effective_at,available_at"
        return [
            Observation(
                r[0], r[1], datetime.fromisoformat(r[2]), datetime.fromisoformat(r[3]),
                r[4], r[5], r[6], r[7], r[8], r[9], tuple(json.loads(r[10])),
                r[11] or "measurement", tuple(json.loads(r[12] or "[]")),
                r[13], r[14], r[15], r[16],
            )
            for r in self.db.execute(q, args)
        ]

    def add_forecast(self, f: Forecast):
        _probability(f.probability, "probability")
        if f.baseline_probability is not None:
            _probability(f.baseline_probability, "baseline_probability")
        if _instant(f.origin) >= _instant(f.horizon_end):
            raise ValueError("forecast origin must precede horizon")
        self.db.execute(
            "INSERT INTO forecasts(forecast_id,event_id,origin,horizon_end,probability,model,baseline_probability) VALUES(?,?,?,?,?,?,?)",
            (f.forecast_id, f.event_id, _instant(f.origin).isoformat(), _instant(f.horizon_end).isoformat(),
             f.probability, f.model, f.baseline_probability),
        )
        self.db.commit()

    def resolve(self, event_id, outcome, resolved_at, vintage="first_release"):
        if type(outcome) is not int or outcome not in (0, 1):
            raise ValueError("outcome must be integer 0 or 1")
        if vintage not in ("first_release", "revision"):
            raise ValueError("unknown outcome vintage")
        self.db.execute(
            "INSERT INTO outcomes VALUES(?,?,?,?)",
            (event_id, _instant(resolved_at).isoformat(), outcome, vintage),
        )
        self.db.commit()

    def scored(self, as_of=None):
        if as_of is None:
            raise ValueError("as_of is required for point-in-time scoring")
        cutoff = _instant(as_of).isoformat()
        return list(self.db.execute(
            "SELECT f.forecast_id,f.probability,f.baseline_probability,o.outcome "
            "FROM forecasts f JOIN outcomes o ON f.event_id=o.event_id "
            "WHERE o.vintage='first_release' AND o.resolved_at>=f.horizon_end "
            "AND o.resolved_at<=? AND f.origin<f.horizon_end "
            "ORDER BY f.forecast_id",
            (cutoff,),
        ))
