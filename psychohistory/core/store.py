import json
import sqlite3
from datetime import datetime
from pathlib import Path

from .models import Forecast, Observation
from .numeric_precision import exact_binary64_real

SCHEMA = """CREATE TABLE IF NOT EXISTS observations(
observation_id TEXT PRIMARY KEY, series TEXT, effective_at TEXT, available_at TEXT,
value REAL, source TEXT, vintage TEXT, revision_type TEXT, quality REAL,
pipeline_position TEXT, ancestry TEXT, evidence_role TEXT DEFAULT 'measurement',
content_ancestry TEXT DEFAULT '[]', carrier TEXT, actor_id TEXT, community_id TEXT,
semantic_variant TEXT);
CREATE TABLE IF NOT EXISTS forecasts(forecast_id TEXT PRIMARY KEY,event_id TEXT,origin TEXT,horizon_end TEXT,probability REAL,model TEXT,baseline_probability REAL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS outcomes(event_id TEXT, resolved_at TEXT, outcome INTEGER CHECK(outcome IN(0,1)), vintage TEXT, PRIMARY KEY(event_id,vintage));
CREATE TABLE IF NOT EXISTS hypotheses(hypothesis_id TEXT PRIMARY KEY,family TEXT,status TEXT,predictive_input INTEGER DEFAULT 0,metadata TEXT);"""


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
        # Validate original numeric types before SQLite coerces them to REAL.
        # An integer beyond binary64 precision or an extended-precision
        # measurement must not silently change on storage.
        if not exact_binary64_real(o.value):
            raise ValueError("observation value must be finite exact binary64")
        if not exact_binary64_real(o.quality) or not 0 <= o.quality <= 1:
            raise ValueError("observation quality must be exact binary64 in [0,1]")
        self.db.execute(
            """INSERT INTO observations(
            observation_id,series,effective_at,available_at,value,source,vintage,
            revision_type,quality,pipeline_position,ancestry,evidence_role,
            content_ancestry,carrier,actor_id,community_id,semantic_variant)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                o.observation_id, o.series, o.effective_at.isoformat(),
                o.available_at.isoformat(), o.value, o.source, o.vintage,
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
        FROM observations WHERE julianday(available_at)<=julianday(?)"""
        args = [as_of.isoformat()]
        if series:
            q += " AND series=?"
            args.append(series)
        q += " ORDER BY julianday(effective_at),julianday(available_at)"
        observations = [
            Observation(
                r[0], r[1], datetime.fromisoformat(r[2]), datetime.fromisoformat(r[3]),
                r[4], r[5], r[6], r[7], r[8], r[9], tuple(json.loads(r[10])),
                r[11] or "measurement", tuple(json.loads(r[12] or "[]")),
                r[13], r[14], r[15], r[16],
            )
            # SQLite julianday() rounds sub-millisecond timestamps.
            # Recheck exact instants before returning observations.
            for r in self.db.execute(q, args)
            if datetime.fromisoformat(r[3]) <= as_of
        ]
        # Preserve sub-millisecond event ordering for directional lag analysis.
        return sorted(
            observations,
            key=lambda o: (o.effective_at, o.available_at, o.observation_id),
        )

    def add_forecast(self, f: Forecast):
        if not 0 <= f.probability <= 1:
            raise ValueError("probability must be in [0,1]")
        self.db.execute(
            "INSERT INTO forecasts(forecast_id,event_id,origin,horizon_end,probability,model,baseline_probability) VALUES(?,?,?,?,?,?,?)",
            (f.forecast_id, f.event_id, f.origin.isoformat(), f.horizon_end.isoformat(),
             f.probability, f.model, f.baseline_probability),
        )
        self.db.commit()

    def resolve(self, event_id, outcome, resolved_at, vintage="first_release"):
        # Never silently turn a fractional outcome into a binary result.
        if type(outcome) is not int or outcome not in (0, 1):
            raise ValueError("outcome must be the integer 0 or 1")
        self.db.execute(
            "INSERT INTO outcomes VALUES(?,?,?,?)",
            (event_id, resolved_at.isoformat(), outcome, vintage),
        )
        self.db.commit()

    def scored(self):
        """Fail closed until registrations and outcome contracts are verified.

        Database rows alone cannot authenticate forecast registration or the
        contract-specified outcome vintage and point-in-time availability.
        """
        return []
