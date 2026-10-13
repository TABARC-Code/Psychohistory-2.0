import pytest

from psychohistory.core.bidirectional import DirectedHypothesis, reciprocal_view


def test_distinct_lags_are_distinct_hypotheses():
    forward = [DirectedHypothesis("technology", "narratives", lag)
               for lag in (2, 14, 30)]
    reverse = DirectedHypothesis("narratives", "technology", 7)
    result = reciprocal_view(iter(forward + [reverse]))
    assert len(result) == 4
    assert all(row["lag_family_size"] == 3 for row in result[:3])
    assert all(row["reverse_lags"] == [7] for row in result[:3])
    assert result[-1]["reverse_lags"] == [2, 14, 30]
    assert all(row["multiplicity_status"] == "UNVERIFIED" for row in result)
    assert all(not row["predictive_input"] for row in result)


def test_same_direction_and_lag_cannot_duplicate():
    with pytest.raises(ValueError):
        reciprocal_view([DirectedHypothesis("a", "b", 1),
                         DirectedHypothesis("a", "b", 1)])


@pytest.mark.parametrize("lag", [True, -1, 1.5, "2", None])
def test_invalid_lag_rejected(lag):
    with pytest.raises(ValueError):
        DirectedHypothesis("a", "b", lag)


@pytest.mark.parametrize("coefficient", [True, float("nan"), float("inf"), 10**400])
def test_invalid_coefficient_rejected(coefficient):
    with pytest.raises(ValueError):
        DirectedHypothesis("a", "b", 1, coefficient=coefficient)
