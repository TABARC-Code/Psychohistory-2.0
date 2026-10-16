from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from psychohistory.core.validation import validate_observations


def row(name, *, quality=1.0, ancestry=("root",), propagation=False):
    now = datetime(2026, 10, 1, tzinfo=UTC)
    return SimpleNamespace(
        observation_id=name, effective_at=now, available_at=now,
        value=1.0, quality=quality, revision_type="none",
        is_propagation=propagation, ancestry=ancestry,
        content_ancestry=ancestry, carrier=None, actor_id=None,
        community_id=None, semantic_variant=None,
    )


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf"), True, False, "0.5"])
def test_bad_quality_rejected(bad):
    result = validate_observations([row("a", quality=bad)], datetime(2026, 10, 2, tzinfo=UTC))
    assert not result["valid"]
    assert any("invalid quality" in e for e in result["errors"])


def test_generator_and_list_equivalence():
    rows = [row("a", ancestry=("x", "x")), row("b", ancestry=("y",))]
    cutoff = datetime(2026, 10, 2, tzinfo=UTC)
    assert validate_observations(iter(rows), cutoff) == validate_observations(rows, cutoff)


def test_duplicate_ancestor_does_not_claim_shared_measurement_source():
    rows = [row("a", ancestry=("x", "x")), row("b", ancestry=("y",))]
    result = validate_observations(rows, datetime(2026, 10, 2, tzinfo=UTC))
    assert result["shared_measurement_ancestry"] == {}
    assert result["measurement_informational_breadth_upper_bound"] == 2


def test_duplicate_ancestor_does_not_claim_shared_content_source():
    rows = [row("a", ancestry=("x", "x"), propagation=True),
            row("b", ancestry=("y",), propagation=True)]
    result = validate_observations(rows, datetime(2026, 10, 2, tzinfo=UTC))
    assert result["shared_content_ancestry"] == {}
    assert result["content_origin_breadth_upper_bound"] == 2
