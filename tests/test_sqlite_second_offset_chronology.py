"""SQLite point-in-time retrieval must support valid UTC offsets with seconds.

SQLite julianday() cannot parse offsets such as +05:30:45 even though Python's
aware datetime model accepts them. An integrity audit must not certify an
observation that retrieval then silently omits.
"""

from datetime import UTC, datetime, timedelta, timezone

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 10, 0, tzinfo=UTC)


def record(identifier, instant, *, series="industrial_supply", role="measurement"):
    return Observation(
        identifier, series, instant, instant, 1.0, "independent-source",
        ancestry=("source-1",),
        evidence_role=role,
        content_ancestry=("narrative-root",) if role == "propagation" else (),
        community_id="community-a" if role == "propagation" else None,
    )


@pytest.mark.parametrize("offset", [
    timedelta(hours=5, minutes=30, seconds=45),
    timedelta(seconds=-30),
    timedelta(hours=5, minutes=30),
])
def test_valid_offset_seconds_survive_point_in_time_retrieval(tmp_path, offset):
    store = Store(tmp_path / "seconds.sqlite")
    instant = NOW.astimezone(timezone(offset))
    store.add_observation(record("shock", instant))
    assert store.audit_stored_observations()["status"] == "VALID"
    assert store.observations_as_of(NOW - timedelta(microseconds=1)) == []
    rows = store.observations_as_of(NOW)
    assert [row.observation_id for row in rows] == ["shock"]
    assert rows[0].available_at.astimezone(UTC) == NOW


def test_second_precision_cutoff_does_not_hide_utc_observations(tmp_path):
    store = Store(tmp_path / "cutoff.sqlite")
    store.add_observation(record("shock", NOW))
    cutoff = NOW.astimezone(timezone(timedelta(seconds=30)))
    assert [o.observation_id for o in store.observations_as_of(cutoff)] == ["shock"]


def test_legacy_second_precision_offset_is_not_silently_dropped(tmp_path):
    store = Store(tmp_path / "legacy.sqlite")
    instant = NOW.astimezone(timezone(timedelta(hours=5, minutes=30, seconds=45)))
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality)
        VALUES(?,?,?,?,?,?)""",
        ("legacy", "industrial_supply", instant.isoformat(),
         instant.isoformat(), 1.0, 1.0),
    )
    store.db.commit()
    assert store.audit_stored_observations()["status"] == "VALID"
    assert [o.observation_id for o in store.observations_as_of(NOW)] == ["legacy"]


def test_microsecond_boundaries_across_second_precision_offsets(tmp_path):
    store = Store(tmp_path / "boundary.sqlite")
    early = NOW - timedelta(microseconds=1)
    late = NOW + timedelta(microseconds=1)
    offset = timezone(timedelta(seconds=45))
    store.add_observation(record("early", early.astimezone(offset)))
    store.add_observation(record("late", late.astimezone(offset)))
    assert [o.observation_id for o in store.observations_as_of(NOW)] == ["early"]
    assert [o.observation_id for o in store.observations_as_of(late)] == [
        "early", "late",
    ]


def test_sorting_uses_absolute_time_with_mixed_offsets(tmp_path):
    store = Store(tmp_path / "ordering.sqlite")
    offset = timezone(timedelta(hours=5, minutes=30, seconds=45))
    store.add_observation(record("later", (NOW + timedelta(seconds=1)).astimezone(offset)))
    store.add_observation(record("earlier", NOW))
    assert [o.observation_id for o in store.observations_as_of(NOW + timedelta(seconds=2))] == [
        "earlier", "later",
    ]


def test_series_filter_keeps_valid_second_precision_offsets(tmp_path):
    store = Store(tmp_path / "series.sqlite")
    instant = NOW.astimezone(timezone(timedelta(seconds=30)))
    store.add_observation(record("industrial", instant))
    store.add_observation(record("health", instant, series="health"))
    assert [o.observation_id for o in store.observations_as_of(NOW, series="health")] == [
        "health",
    ]


def test_pipeline_receives_propagation_with_second_precision_offset(tmp_path):
    store = Store(tmp_path / "pipeline.sqlite")
    instant = NOW.astimezone(timezone(timedelta(seconds=30)))
    store.add_observation(record("narrative", instant, series="g1:meme", role="propagation"))
    result = evaluate(store, NOW)
    assert result["n_observations"] == 1
    assert result["g1_memetics"]["propagation"]["events"] == 1
    assert result["g1_memetics"]["predictive_input"] is False
