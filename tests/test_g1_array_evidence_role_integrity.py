"""Malformed array-valued evidence roles must not crash or silently enter G1."""

from datetime import UTC, datetime

import numpy as np
import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 26, 1, tzinfo=UTC)


def observation(identifier, role):
    return Observation(
        identifier, "g1:non_ai_industrial", NOW, NOW, 1.0, "source",
        evidence_role=role, ancestry=("collector",),
        content_ancestry=("original",), community_id="A",
    )


@pytest.mark.parametrize("role", [
    np.array(["propagation", "measurement"]),
    np.array(["propagation"]),
])
def test_array_role_is_not_a_boolean_propagation_classification(role):
    event = observation("bad", role)
    assert event.is_propagation is False
    report = validate_observations([event], NOW)
    assert report["valid"] is False
    assert any("invalid evidence role" in issue for issue in report["errors"])


def test_array_role_is_rejected_before_storage(tmp_path):
    store = Store(tmp_path / "role.db")
    with pytest.raises(ValueError, match="evidence role"):
        store.add_observation(
            observation("bad", np.array(["propagation", "measurement"]))
        )
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


def test_direct_g1_refuses_malformed_role_instead_of_dropping_it():
    valid = observation("valid", "propagation")
    invalid = observation("bad", np.array(["propagation", "measurement"]))
    report = analyse_memetic_observations([valid, invalid])
    assert report["status"] == "UNRESOLVED"
    assert report["predictive_input"] is False
    assert "evidence role" in report["reason"]


def test_direct_g1_still_ignores_valid_ordinary_measurements():
    valid = observation("valid", "propagation")
    ordinary = observation("ordinary", "measurement")
    report = analyse_memetic_observations([valid, ordinary])
    assert report["status"] == "CANDIDATE_NOT_ADMITTED"
    assert report["propagation"]["events"] == 1
    assert report["predictive_input"] is False
