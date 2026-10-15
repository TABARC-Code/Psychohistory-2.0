from datetime import datetime, timezone
import pytest
from psychohistory.core.store import Store


def test_outcomes_reject_coercion(tmp_path):
    store = Store(tmp_path / "outcomes.sqlite")
    when = datetime(2026, 10, 15, tzinfo=timezone.utc)
    for invalid in (0.5, 1.5, True, False, "1", None, -1, 2):
        with pytest.raises(ValueError):
            store.resolve("example", invalid, when)
    assert list(store.db.execute("SELECT * FROM outcomes")) == []


def test_binary_integer_outcome_allowed(tmp_path):
    store = Store(tmp_path / "outcomes.sqlite")
    when = datetime(2026, 10, 15, tzinfo=timezone.utc)
    store.resolve("example", 1, when)
    assert store.db.execute("SELECT outcome FROM outcomes").fetchone()[0] == 1
