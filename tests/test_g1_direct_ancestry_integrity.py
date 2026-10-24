"""Direct G1 diagnostics must not manufacture ancestry from malformed metadata."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


WHEN = datetime(2026, 10, 24, 12, tzinfo=UTC)


def event(index, **changes):
    fields = {
        "observation_id": f"event-{index}",
        "series": "g1:meme",
        "effective_at": WHEN,
        "available_at": WHEN,
        "value": 1.0,
        "source": "observed",
        "evidence_role": "propagation",
        "ancestry": ("collector",),
        "content_ancestry": ("shared-root",),
        "community_id": f"community-{index}",
    }
    fields.update(changes)
    return Observation(**fields)


@pytest.mark.parametrize(
    "bad",
    ["root", {"root": 1}, ("root", 2), None, 3],
)
def test_direct_g1_rejects_malformed_content_ancestry(bad):
    result = analyse_memetic_observations([
        event(1, content_ancestry=bad),
        event(2),
    ])
    assert result["status"] == "UNRESOLVED"
    assert "ancestry" in result["reason"]
    assert result["predictive_input"] is False


@pytest.mark.parametrize("bad", ["collector", {"collector": 1}, ("collector", None)])
def test_direct_g1_rejects_malformed_measurement_ancestry(bad):
    result = analyse_memetic_observations([event(1, ancestry=bad), event(2)])
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


def test_valid_direct_g1_lineages_keep_existing_bounds():
    result = analyse_memetic_observations([event(1), event(2)])
    resonance = result["social_resonance"]
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert resonance["shared_lineage_event_fraction_lower_bound"] == 1.0
    assert resonance["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1.0
    assert result["predictive_input"] is False


def test_unrecorded_ancestry_is_a_valid_empty_collection():
    result = analyse_memetic_observations([
        event(1, ancestry=(), content_ancestry=()),
        event(2),
    ])
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["social_resonance"]["content_ancestry_coverage_fraction"] == 0.5
    assert result["predictive_input"] is False
