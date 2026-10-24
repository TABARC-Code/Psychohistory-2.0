"""Outcome persistence checks source clocks and labels before storing evidence.

Local outcome rows are not authenticated Outcome Contracts and cannot enable
forecast scoring or G23 admission.
"""

from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.core.store import Store


WHEN = datetime(2026, 10, 29, 9, 30, tzinfo=UTC)


@pytest.mark.parametrize("event_id", ["", "   ", None, True, 123])
def test_outcome_rejects_invalid_event_identifiers(tmp_path, event_id):
    store = Store(tmp_path / "outcomes.sqlite")
    with pytest.raises(ValueError):
        store.resolve(event_id, 1, WHEN)
    assert store.db.execute("SELECT COUNT(*) FROM outcomes").fetchone()[0] == 0


@pytest.mark.parametrize("vintage", ["", "   ", None, False, 2])
def test_outcome_rejects_invalid_vintage_labels(tmp_path, vintage):
    store = Store(tmp_path / "outcomes.sqlite")
    with pytest.raises(ValueError):
        store.resolve("example", 1, WHEN, vintage=vintage)
    assert store.db.execute("SELECT COUNT(*) FROM outcomes").fetchone()[0] == 0


class NoOffset(tzinfo):
    def utcoffset(self, dt):
        return None


@pytest.mark.parametrize("resolved_at", [
    WHEN.replace(tzinfo=None),
    None,
    "2026-10-29T09:30:00+00:00",
    datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
    datetime.max.replace(tzinfo=timezone(-timedelta(hours=1))),
    WHEN.replace(tzinfo=NoOffset()),
])
def test_outcome_rejects_invalid_utc_clocks(tmp_path, resolved_at):
    store = Store(tmp_path / "outcomes.sqlite")
    with pytest.raises(ValueError):
        store.resolve("example", 1, resolved_at)
    assert store.db.execute("SELECT COUNT(*) FROM outcomes").fetchone()[0] == 0


def test_outcome_accepts_valid_offset_and_separate_revision(tmp_path):
    store = Store(tmp_path / "outcomes.sqlite")
    offset = timezone(timedelta(hours=5, minutes=30, seconds=45))
    local = WHEN.astimezone(offset)
    store.resolve("example", 0, local)
    store.resolve("example", 1, WHEN + timedelta(days=7), vintage="revision_1")
    rows = list(store.db.execute(
        "SELECT event_id,resolved_at,outcome,vintage,typeof(outcome) "
        "FROM outcomes ORDER BY vintage"
    ))
    assert len(rows) == 2
    assert rows[0] == ("example", local.isoformat(), 0, "first_release", "integer")
    assert datetime.fromisoformat(rows[0][1]).astimezone(UTC) == WHEN
    assert rows[1][2:] == (1, "revision_1", "integer")
    assert store.scored() == []
