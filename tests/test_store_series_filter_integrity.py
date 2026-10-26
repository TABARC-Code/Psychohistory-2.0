"""A requested evidence series must never silently become an all-domain query."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store


AS_OF = datetime(2026, 10, 26, 12, tzinfo=UTC)


def _populate(store):
    for name, series in (
        ("shock", "industrial"),
        ("narrative", "g1:narrative"),
    ):
        store.add_observation(Observation(
            observation_id=name,
            series=series,
            effective_at=AS_OF,
            available_at=AS_OF,
            value=1.0,
            source="independent-source",
            ancestry=(name,),
        ))


@pytest.mark.parametrize("invalid", ("", " ", " industrial", "industrial ", 0, False, []))
def test_invalid_series_selector_fails_closed(tmp_path, invalid):
    store = Store(tmp_path / "observations.db")
    _populate(store)
    with pytest.raises(ValueError, match="series"):
        store.observations_as_of(AS_OF, series=invalid)


def test_explicit_series_selector_cannot_expand_to_other_domains(tmp_path):
    store = Store(tmp_path / "observations.db")
    _populate(store)
    assert [row.observation_id for row in store.observations_as_of(
        AS_OF, series="industrial"
    )] == ["shock"]
    assert [row.observation_id for row in store.observations_as_of(
        AS_OF, series="g1:narrative"
    )] == ["narrative"]
    assert {row.observation_id for row in store.observations_as_of(
        AS_OF, series=None
    )} == {"shock", "narrative"}
