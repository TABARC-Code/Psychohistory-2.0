import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from .models import Forecast, Observation
from .numeric_precision import exact_binary64_real
from .validation import (
    _aware_instant, _valid_ancestry, _valid_optional_label, _valid_primary_label,
)

SCHEMA = """CREATE TABLE IF NOT EXISTS observations(
observation_id TEXT PRIMARY KEY, series TEXT, effective_at TEXT, available_at TEXT,
value REAL, source TEXT, vintage TEXT, revision_type TEXT, quality REAL,
pipeline_position TEXT, ancestry TEXT, evidence_role TEXT DEFAULT 'measurement',
content_ancestry TEXT DEFAULT '[]', carrier TEXT, actor_id TEXT, community_id TEXT,
semantic_variant TEXT);
CREATE TABLE IF NOT EXISTS forecasts(forecast_id TEXT PRIMARY KEY,event_id TEXT,origin TEXT,horizon_end TEXT,probability REAL,model TEXT,baseline_probability REAL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS outcomes(event_id TEXT, resolved_at TEXT, outcome INTEGER CHECK(outcome IN(0,1)), vintage TEXT, PRIMARY KEY(event_id,vintage));
CREATE TABLE IF NOT EXISTS hypotheses(hypothesis_id TEXT PRIMARY KEY,family TEXT,status TEXT,predictive_input INTEGER DEFAULT 0,metadata TEXT);"""

def _valid_stored_ancestry(raw):
    """Legacy SQL NULL means unrecorded ancestry, not a claimed source.

    Other values must be JSON arrays of non-blank source identifiers.
    Converting a JSON string or object directly to tuple would manufacture
    ancestry from its characters or keys.
    """
    if raw is None:
        return True
    if not isinstance(raw, str):
        return False
    try:
        decoded = json.loads(raw)
    except (TypeError, ValueError):
        return False
    return isinstance(decoded, list) and _valid_ancestry(decoded)


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
        # SQLite permits NULL TEXT primary keys and blank series labels.
        # Refuse malformed identities before evidence can enter the ledger.
        for field in ("observation_id", "series", "source", "vintage"):
            label = getattr(o, field)
            if not _valid_primary_label(label):
                raise ValueError(f"observation {field} must be a canonical non-blank string")
        # Validate original numeric types before SQLite coerces them to REAL.
        # An integer beyond binary64 precision or an extended-precision
        # measurement must not silently change on storage.
        if not exact_binary64_real(o.value):
            raise ValueError("observation value must be finite exact binary64")
        if not exact_binary64_real(o.quality) or not 0 <= o.quality <= 1:
            raise ValueError("observation quality must be exact binary64 in [0,1]")
        # Persist only clocks that can be ordered as real UTC instants.
        # A naive stored clock would later crash comparisons with an aware cutoff.
        if not _aware_instant(o.effective_at) or not _aware_instant(o.available_at):
            raise ValueError("observation clocks must be UTC-convertible aware datetimes")
        # Advance notices are valid ordinary measurements, but cannot be
        # stored as observations of propagation before the event occurred.
        if (o.is_propagation
                and o.effective_at.astimezone(UTC) > o.available_at.astimezone(UTC)):
            raise ValueError("propagation chronology: event follows first availability")
        if not _valid_ancestry(o.ancestry) or not _valid_ancestry(o.content_ancestry):
            raise ValueError("observation ancestry must be lists or tuples of non-blank IDs")
        # Evidence role determines whether an event enters G1 propagation or
        # ordinary measurement. Do not persist a role that retrieval might
        # silently reclassify as ordinary evidence.
        if (type(o.evidence_role) is not str
                or o.evidence_role not in ("measurement", "propagation")):
            raise ValueError("observation evidence role must be measurement or propagation")
        for field in (
            "pipeline_position", "carrier", "actor_id",
            "community_id", "semantic_variant",
        ):
            if not _valid_optional_label(getattr(o, field)):
                raise ValueError(f"observation {field} must be non-blank text or NULL")
        # SQLite binds some valid NumPy scalars as BLOBs unless normalised.
        # Convert only after exact-binary64 validation has succeeded.
        self.db.execute(
            """INSERT INTO observations(
            observation_id,series,effective_at,available_at,value,source,vintage,
            revision_type,quality,pipeline_position,ancestry,evidence_role,
            content_ancestry,carrier,actor_id,community_id,semantic_variant)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                o.observation_id, o.series, o.effective_at.isoformat(),
                o.available_at.isoformat(), float(o.value), o.source, o.vintage,
                o.revision_type, float(o.quality), o.pipeline_position,
                json.dumps(o.ancestry), o.evidence_role,
                json.dumps(o.content_ancestry), o.carrier, o.actor_id,
                o.community_id, o.semantic_variant,
            ),
        )
        self.db.commit()

    def audit_stored_observations(self):
        """Read-only check of legacy evidence that predates insertion guards.

        SQLite's julianday() silently excludes unparseable availability clocks.
        Checking only selected rows would therefore conceal corrupt evidence.
        Audit the full stored population before any point-in-time selection.
        """
        issues = []
        checked = 0
        for (identifier, series, source, vintage, effective, available, value,
             quality, ancestry, content_ancestry, evidence_role,
             pipeline_position, carrier, actor_id, community_id,
             semantic_variant) in self.db.execute(
            "SELECT observation_id,series,source,vintage,effective_at,available_at, "
            "value,quality,ancestry,content_ancestry,evidence_role, "
            "pipeline_position,carrier,actor_id,community_id,semantic_variant "
            "FROM observations ORDER BY observation_id"
        ):
            checked += 1
            invalid = []
            for field, label in (("observation_id", identifier), ("series", series)):
                if not _valid_primary_label(label):
                    invalid.append(field)
            # Legacy SQL NULL source/vintage means unrecorded, not a
            # fabricated publication or release. Explicit malformed labels
            # are still corrupt. New writes always require both fields.
            for field, label in (("source", source), ("vintage", vintage)):
                if label is not None and not _valid_primary_label(label):
                    invalid.append(field)
            for field, raw in (
                ("effective_at", effective), ("available_at", available)
            ):
                try:
                    parsed = datetime.fromisoformat(raw)
                except (TypeError, ValueError, OverflowError):
                    invalid.append(field)
                else:
                    if not _aware_instant(parsed):
                        invalid.append(field)
            if (evidence_role == "propagation"
                    and "effective_at" not in invalid
                    and "available_at" not in invalid
                    and datetime.fromisoformat(effective).astimezone(UTC)
                    > datetime.fromisoformat(available).astimezone(UTC)):
                invalid.append("propagation chronology")
            if not exact_binary64_real(value):
                invalid.append("value")
            if not exact_binary64_real(quality) or not 0 <= quality <= 1:
                invalid.append("quality")
            if not _valid_stored_ancestry(ancestry):
                invalid.append("ancestry")
            if not _valid_stored_ancestry(content_ancestry):
                invalid.append("content_ancestry")
            # SQL NULL is the existing legacy convention for an unrecorded
            # role. Explicit empty, unknown or non-text roles are corrupt;
            # retrieval must not turn them into ordinary measurements.
            if (evidence_role is not None and
                    (type(evidence_role) is not str or evidence_role not in
                     ("measurement", "propagation"))):
                invalid.append("evidence_role")
            for field, label in (
                ("pipeline_position", pipeline_position),
                ("carrier", carrier), ("actor_id", actor_id),
                ("community_id", community_id),
                ("semantic_variant", semantic_variant),
            ):
                if not _valid_optional_label(label):
                    invalid.append(field)
            if invalid:
                issues.append({"observation_id": identifier, "fields": invalid})
        return {
            "status": "UNRESOLVED" if issues else "VALID",
            "checked": checked,
            "issues": issues,
            "predictive_input": False,
        }

    def observations_as_of(self, as_of: datetime, series=None):
        if not _aware_instant(as_of):
            raise ValueError("as_of must be a UTC-convertible aware datetime")
        audit = self.audit_stored_observations()
        if audit["status"] != "VALID":
            raise ValueError(
                f"stored observation integrity unresolved: {len(audit['issues'])} invalid rows"
            )
        # SQLite julianday() does not understand every UTC-convertible ISO
        # offset (notably offsets with seconds). It can silently omit valid
        # evidence and rounds sub-millisecond times. The full-population
        # integrity audit already scans every record, so select by exact
        # Python UTC instants rather than using SQLite as a time filter.
        q = """SELECT observation_id,series,effective_at,available_at,value,source,
        vintage,revision_type,quality,pipeline_position,ancestry,evidence_role,
        content_ancestry,carrier,actor_id,community_id,semantic_variant
        FROM observations"""
        args = []
        if series:
            q += " WHERE series=?"
            args.append(series)
        cutoff = as_of.astimezone(UTC)
        observations = [
            Observation(
                r[0], r[1], datetime.fromisoformat(r[2]), datetime.fromisoformat(r[3]),
                r[4], r[5], r[6], r[7], r[8], r[9], tuple(json.loads(r[10] or "[]")),
                r[11] or "measurement", tuple(json.loads(r[12] or "[]")),
                r[13], r[14], r[15], r[16],
            )
            for r in self.db.execute(q, args)
            if datetime.fromisoformat(r[3]).astimezone(UTC) <= cutoff
        ]
        # Absolute UTC sorting also handles mixed offsets and repeated local
        # clock labels. Preserve exact microsecond ordering and stable ties.
        return sorted(
            observations,
            key=lambda o: (
                o.effective_at.astimezone(UTC),
                o.available_at.astimezone(UTC),
                o.observation_id,
            ),
        )

    def add_forecast(self, f: Forecast):
        # Database persistence cannot authenticate immutable registration or
        # admit a forecast, but it must not corrupt its probability or clocks.
        if any(
            not _valid_primary_label(identifier)
            for identifier in (f.forecast_id, f.event_id, f.model)
        ):
            raise ValueError("forecast identifiers and model must be non-blank strings")
        if not exact_binary64_real(f.probability) or not 0 <= f.probability <= 1:
            raise ValueError("probability must be exact binary64 in [0,1]")
        if (f.baseline_probability is not None
                and (not exact_binary64_real(f.baseline_probability)
                     or not 0 <= f.baseline_probability <= 1)):
            raise ValueError("baseline probability must be exact binary64 in [0,1]")
        if (not _aware_instant(f.origin) or not _aware_instant(f.horizon_end)
                or f.horizon_end.astimezone(UTC) <= f.origin.astimezone(UTC)):
            raise ValueError("forecast horizon must follow a valid UTC origin")
        # SQLite binds some NumPy scalars as BLOBs. Normalise only after
        # exact-value checks so stored forecasts retain their measurements.
        self.db.execute(
            "INSERT INTO forecasts(forecast_id,event_id,origin,horizon_end,probability,model,baseline_probability) VALUES(?,?,?,?,?,?,?)",
            (f.forecast_id, f.event_id, f.origin.isoformat(), f.horizon_end.isoformat(),
             float(f.probability), f.model,
             float(f.baseline_probability) if f.baseline_probability is not None else None),
        )
        self.db.commit()

    def resolve(self, event_id, outcome, resolved_at, vintage="first_release"):
        # An outcome is evidence, not a verified Outcome Contract. Preserve
        # the original binary value, source label and actual UTC instant.
        # Neither this insertion nor the vintage label admits forecast scoring.
        if not _valid_primary_label(event_id) or not _valid_primary_label(vintage):
            raise ValueError("outcome event and vintage must be non-blank strings")
        if type(outcome) is not int or outcome not in (0, 1):
            raise ValueError("outcome must be the integer 0 or 1")
        if not _aware_instant(resolved_at):
            raise ValueError("outcome resolved_at must be a UTC-convertible aware datetime")
        self.db.execute(
            "INSERT INTO outcomes VALUES(?,?,?,?)",
            (event_id, resolved_at.isoformat(), outcome, vintage),
        )
        self.db.commit()

    def audit_stored_outcomes(self):
        """Read-only audit of historical outcome evidence.

        Legacy SQLite tables can contain NULL outcomes despite a CHECK
        constraint, and composite primary keys permit NULL identifiers.
        Neither a valid row nor this audit authenticates an Outcome Contract.
        """
        issues = []
        checked = 0
        rows = self.db.execute(
            "SELECT rowid,event_id,resolved_at,outcome,vintage "
            "FROM outcomes ORDER BY rowid"
        )
        for rowid, event_id, resolved_at, outcome, vintage in rows:
            checked += 1
            invalid = []
            if not _valid_primary_label(event_id):
                invalid.append("event_id")
            if not _valid_primary_label(vintage):
                invalid.append("vintage")
            if type(outcome) is not int or outcome not in (0, 1):
                invalid.append("outcome")
            try:
                instant = datetime.fromisoformat(resolved_at)
            except (TypeError, ValueError, OverflowError):
                invalid.append("resolved_at")
            else:
                if not _aware_instant(instant):
                    invalid.append("resolved_at")
            if invalid:
                issues.append({
                    "rowid": rowid,
                    "event_id": event_id,
                    "vintage": vintage,
                    "fields": invalid,
                })
        return {
            "status": "UNRESOLVED" if issues else "VALID",
            "checked": checked,
            "issues": issues,
            "predictive_input": False,
        }

    def scored(self):
        """Fail closed until registrations and outcome contracts are verified.

        Database rows alone cannot authenticate forecast registration or the
        contract-specified outcome vintage and point-in-time availability.
        """
        return []
