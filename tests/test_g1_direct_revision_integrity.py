"""Direct G1 revision metadata must respect the measurement boundary."""

from datetime import UTC, datetime

import numpy as np
import pytest

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 26, 1, tzinfo=UTC)


def event(identifier, revision_type="none"):
    return Observation(
        observation_id=identifier,
        series="g1:industrial-narrative",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="publisher",
        revision_type=revision_type,
        evidence_role="propagation",
        ancestry=("collector",),
        content_ancestry=("shared-root",),
        community_id=identifier,
    )


@pytest.mark.parametrize("bad_revision", [
    None,
    1,
    ["none"],
    {"revision": "none"},
    np.array(["none"]),
])
def test_direct_g1_rejects_invalid_revision_classification(bad_revision):
    rows = [event("community-a"), event("community-b", bad_revision)]
    assert validate_observations(rows, NOW)["valid"] is False
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert "revision" in result["reason"]
    assert result["predictive_input"] is False


def test_known_revision_classifications_remain_accepted():
    rows = [event("community-a"), event("community-b", "correction")]
    assert validate_observations(rows, NOW)["valid"] is True
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["social_resonance"]["shared_lineage_event_fraction_lower_bound"] == 1.0
    assert result["predictive_input"] is False


def test_unknown_textual_revision_retains_existing_warning_policy():
    rows = [event("community-a"), event("community-b", "legacy_category")]
    validation = validate_observations(rows, NOW)
    assert validation["valid"] is True
    assert any("unknown revision" in warning for warning in validation["warnings"])
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["predictive_input"] is False
