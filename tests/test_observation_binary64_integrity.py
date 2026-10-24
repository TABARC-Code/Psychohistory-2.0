"""Preserve source observation numbers before binary64 and SQLite conversion."""

from datetime import UTC, datetime

import numpy as np
import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations


NOW = datetime(2026, 10, 24, 9, tzinfo=UTC)


def observation(name="source", *, value=1.0, quality=1.0):
    return Observation(
        name, "industrial_supply", NOW, NOW, value,
        "first-release", quality=quality, ancestry=("independent-source",),
    )


def test_validation_rejects_integer_measurement_lost_by_binary64():
    result = validate_observations([observation(value=2**53 + 1)], NOW)
    assert result["valid"] is False
    assert any("invalid numeric value" in error for error in result["errors"])


def test_validation_rejects_underflowed_extended_precision_measurement():
    value = np.longdouble("1e-4000")
    if value == 0:
        pytest.skip("extended precision unavailable")
    assert float(value) == 0.0
    result = validate_observations([observation(value=value)], NOW)
    assert result["valid"] is False
    assert any("invalid numeric value" in error for error in result["errors"])


def test_validation_rejects_lossy_extended_precision_quality():
    quality = np.longdouble("0.5000000000000000001")
    if quality == float(quality):
        pytest.skip("extended precision unavailable")
    result = validate_observations([observation(quality=quality)], NOW)
    assert result["valid"] is False
    assert any("invalid quality" in error for error in result["errors"])


@pytest.mark.parametrize("bad", [2**53 + 1, True, float("inf")])
def test_store_refuses_invalid_raw_values_before_persistence(tmp_path, bad):
    store = Store(tmp_path / "measurements.sqlite")
    with pytest.raises(ValueError, match="value"):
        store.add_observation(observation(value=bad))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


def test_store_refuses_extended_precision_underflow_before_persistence(tmp_path):
    value = np.longdouble("1e-4000")
    if value == 0:
        pytest.skip("extended precision unavailable")
    store = Store(tmp_path / "measurements.sqlite")
    with pytest.raises(ValueError, match="value"):
        store.add_observation(observation(value=value))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


def test_store_refuses_lossy_quality_before_persistence(tmp_path):
    store = Store(tmp_path / "measurements.sqlite")
    with pytest.raises(ValueError, match="quality"):
        store.add_observation(observation(quality=2**53 + 1))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


def test_exact_binary64_measurements_remain_usable(tmp_path):
    row = observation(value=2**53, quality=0.5)
    assert validate_observations([row], NOW)["valid"] is True
    store = Store(tmp_path / "measurements.sqlite")
    store.add_observation(row)
    restored = store.observations_as_of(NOW)
    assert len(restored) == 1
    assert restored[0].value == 2**53
    assert restored[0].quality == 0.5
