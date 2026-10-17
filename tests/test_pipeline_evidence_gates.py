from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 16, 7, 30, tzinfo=UTC)


def observation(name, *, value=1.0, quality=1.0, propagation=True,
                available_at=NOW):
    return SimpleNamespace(
        observation_id=name, effective_at=NOW, available_at=available_at,
        value=value, quality=quality, revision_type="none",
        is_propagation=propagation, ancestry=("shared",),
        content_ancestry=("shared",), carrier="social", actor_id=name,
        community_id="c1", semantic_variant="v1",
    )


class UnverifiedStore:
    def __init__(self, rows):
        self.rows = rows
        self.scored_called = False

    def observations_as_of(self, as_of):
        return self.rows

    def scored(self):
        self.scored_called = True
        return [("future", 0.99, 0.5, 1)]


def test_invalid_g1_quality_blocks_diagnostics():
    result = evaluate(UnverifiedStore([observation("bad", quality=float("nan"))]), NOW)
    assert not result["g1_measurement"]["valid"]
    assert result["g1_memetics"]["status"] == "UNRESOLVED"
    assert result["g1_memetics"]["predictive_input"] is False


def test_invalid_g1_value_blocks_diagnostics():
    result = evaluate(UnverifiedStore([observation("bad", value=float("inf"))]), NOW)
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_duplicate_propagation_id_blocks_diagnostics():
    result = evaluate(
        UnverifiedStore([observation("same"), observation("same")]), NOW
    )
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_future_propagation_blocks_diagnostics():
    future = observation("future", available_at=NOW + timedelta(microseconds=1))
    result = evaluate(UnverifiedStore([future]), NOW)
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_invalid_non_g1_measurement_does_not_block_valid_g1():
    rows = [
        observation("meme"),
        observation("industrial", quality=-1, propagation=False),
    ]
    result = evaluate(UnverifiedStore(rows), NOW)
    assert not result["measurement"]["valid"]
    assert result["g1_measurement"]["valid"]
    assert result["g1_memetics"]["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["g1_memetics"]["predictive_input"] is False


def test_no_propagation_remains_unresolved():
    result = evaluate(
        UnverifiedStore([observation("industrial", propagation=False)]), NOW
    )
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_unverified_outcomes_never_reach_scoring():
    store = UnverifiedStore([observation("meme")])
    result = evaluate(store, NOW)
    assert not store.scored_called
    assert result["scoring"]["status"] == "UNMEASURED"
    assert result["scoring"]["n"] == 0
    assert result["claims"]["overall_brier"] == "UNMEASURED"
    assert "registration" in result["scoring"]["reason"]
