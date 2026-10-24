"""Ensure validated NumPy scalar measurements remain SQLite REAL values."""

from datetime import UTC, datetime

import numpy as np
import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations


NOW = datetime(2026, 10, 24, 10, tzinfo=UTC)


def observation(*, value=1.0, quality=1.0):
    return Observation(
        "numpy-source", "industrial_supply", NOW, NOW, value,
        "independent-release", quality=quality, ancestry=("source-1",),
    )


@pytest.mark.parametrize("value", [
    np.int32(7), np.int64(7), np.uint64(7),
    np.float32(0.5), np.float64(0.5),
])
def test_valid_numpy_value_is_stored_as_sqlite_real(tmp_path, value):
    row = observation(value=value)
    assert validate_observations([row], NOW)["valid"]
    store = Store(tmp_path / "observations.sqlite")
    store.add_observation(row)
    storage_type, stored_value = store.db.execute(
        "SELECT typeof(value), value FROM observations"
    ).fetchone()
    assert storage_type == "real"
    assert stored_value == float(value)
    restored = store.observations_as_of(NOW)
    assert len(restored) == 1
    assert restored[0].value == float(value)
    assert validate_observations(restored, NOW)["valid"]


@pytest.mark.parametrize("quality", [np.int64(1), np.float32(0.5)])
def test_valid_numpy_quality_is_stored_as_sqlite_real(tmp_path, quality):
    row = observation(quality=quality)
    assert validate_observations([row], NOW)["valid"]
    store = Store(tmp_path / "observations.sqlite")
    store.add_observation(row)
    storage_type, stored_quality = store.db.execute(
        "SELECT typeof(quality), quality FROM observations"
    ).fetchone()
    assert storage_type == "real"
    assert stored_quality == float(quality)
    restored = store.observations_as_of(NOW)
    assert len(restored) == 1
    assert restored[0].quality == float(quality)
    assert validate_observations(restored, NOW)["valid"]
