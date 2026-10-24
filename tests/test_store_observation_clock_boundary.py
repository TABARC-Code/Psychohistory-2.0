"""SQLite observation clocks must survive the shared UTC validation boundary."""

from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store


NOW = datetime(2026, 10, 24, 10, 0, tzinfo=UTC)


class UndefinedOffset(tzinfo):
    def utcoffset(self, dt):
        return None

    def dst(self, dt):
        return None


class BrokenOffset(tzinfo):
    def utcoffset(self, dt):
        raise ValueError("timezone provider failed")

    def dst(self, dt):
        return None


BAD_CLOCKS = [
    datetime(2026, 10, 24, 10, 0),
    datetime(2026, 10, 24, 10, 0, tzinfo=UndefinedOffset()),
    datetime(2026, 10, 24, 10, 0, tzinfo=BrokenOffset()),
    datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
    datetime.max.replace(tzinfo=timezone(timedelta(hours=-1))),
    "2026-10-24T10:00:00Z",
]


def observation(*, effective_at=NOW, available_at=NOW):
    return Observation(
        "shock-1", "industrial_supply", effective_at, available_at,
        1.0, "independent-release", ancestry=("record-1",),
    )


@pytest.mark.parametrize("bad", BAD_CLOCKS)
@pytest.mark.parametrize("field", ["effective_at", "available_at"])
def test_invalid_clocks_rejected_before_persistence(tmp_path, field, bad):
    store = Store(tmp_path / "clock.sqlite")
    with pytest.raises(ValueError, match="UTC-convertible"):
        store.add_observation(observation(**{field: bad}))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize("bad", BAD_CLOCKS)
def test_invalid_asof_rejected_before_sqlite_query(tmp_path, bad):
    store = Store(tmp_path / "clock.sqlite")
    with pytest.raises(ValueError, match="UTC-convertible"):
        store.observations_as_of(bad)


def test_valid_non_utc_clocks_roundtrip_at_exact_instant(tmp_path):
    store = Store(tmp_path / "clock.sqlite")
    offset = timezone(timedelta(hours=5, minutes=30))
    equivalent = NOW.astimezone(offset)
    store.add_observation(observation(effective_at=equivalent, available_at=equivalent))
    rows = store.observations_as_of(NOW)
    assert len(rows) == 1
    assert rows[0].effective_at.astimezone(UTC) == NOW
    assert rows[0].available_at.astimezone(UTC) == NOW


def test_microsecond_availability_is_not_backdated(tmp_path):
    store = Store(tmp_path / "clock.sqlite")
    future = NOW + timedelta(microseconds=1)
    store.add_observation(observation(available_at=future))
    assert store.observations_as_of(NOW) == []
    assert len(store.observations_as_of(future)) == 1
