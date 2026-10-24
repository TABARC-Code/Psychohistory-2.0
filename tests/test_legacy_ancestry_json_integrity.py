"""Ancestry is a typed list of source IDs, not an arbitrary JSON iterable."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 12, tzinfo=UTC)


def _legacy(store, identifier, *, ancestry="[]", content_ancestry="[]"):
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality,
         ancestry,content_ancestry)
        VALUES(?,?,?,?,?,?,?,?)""",
        (identifier, "g1:meme", NOW.isoformat(), NOW.isoformat(),
         1.0, 1.0, ancestry, content_ancestry),
    )
    store.db.commit()


@pytest.mark.parametrize(("column", "payload"), [
    ("ancestry", '"root"'),
    ("ancestry", '{"root": 1}'),
    ("ancestry", '[null]'),
    ("ancestry", '[""]'),
    ("ancestry", 'not-json'),
    ("content_ancestry", '"lineage"'),
    ("content_ancestry", '{"lineage": true}'),
    ("content_ancestry", '[7]'),
    ("content_ancestry", '["   "]'),
    ("content_ancestry", 'not-json'),
])
def test_legacy_invalid_ancestry_fails_closed(tmp_path, column, payload):
    store = Store(tmp_path / "legacy.db")
    _legacy(store, "bad-ancestry", **{column: payload})
    before = store.db.total_changes
    result = store.audit_stored_observations()
    assert result["status"] == "UNRESOLVED"
    assert result["issues"] == [{
        "observation_id": "bad-ancestry", "fields": [column],
    }]
    assert result["predictive_input"] is False
    assert store.db.total_changes == before
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        evaluate(store, NOW)


@pytest.mark.parametrize(("column", "value"), [
    ("ancestry", "root"),
    ("ancestry", ("",)),
    ("ancestry", ("root", 3)),
    ("content_ancestry", "lineage"),
    ("content_ancestry", (" ",)),
    ("content_ancestry", ("lineage", None)),
])
def test_new_invalid_ancestry_rejected_before_storage(tmp_path, column, value):
    store = Store(tmp_path / "new.db")
    fields = {
        "observation_id": "bad-new", "series": "g1:meme",
        "effective_at": NOW, "available_at": NOW, "value": 1.0,
        "source": "source", "evidence_role": "propagation",
    }
    fields[column] = value
    with pytest.raises(ValueError, match="ancestry"):
        store.add_observation(Observation(**fields))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


def test_valid_lineages_and_legacy_missing_ancestry_remain_readable(tmp_path):
    store = Store(tmp_path / "valid.db")
    store.add_observation(Observation(
        "good", "g1:meme", NOW, NOW, 1.0, "source",
        evidence_role="propagation",
        ancestry=("collector-1",), content_ancestry=("root-1", "root-2"),
    ))
    _legacy(store, "missing", ancestry=None, content_ancestry=None)
    assert store.audit_stored_observations()["status"] == "VALID"
    rows = {o.observation_id: o for o in store.observations_as_of(NOW)}
    assert rows["good"].ancestry == ("collector-1",)
    assert rows["good"].content_ancestry == ("root-1", "root-2")
    assert rows["missing"].ancestry == ()
    assert rows["missing"].content_ancestry == ()
