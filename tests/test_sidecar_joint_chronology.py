"""Joint chronology regressions for the diagnostic cross-domain lag audit.

Marginal lead and preannouncement counts cannot identify the overlap between
an apparent lead and a target that was already publicly announced.
"""
from datetime import UTC, datetime, timedelta

from psychohistory.core.bidirectional import DirectedHypothesis
from psychohistory.core.models import Observation
from psychohistory.sidecars.lag_audit import audit_directional_lags


BASE = datetime(2026, 10, 1, tzinfo=UTC)
CUTOFF = BASE + timedelta(days=10)


def observation(identifier, series, effective_day, available_day):
    return Observation(
        identifier, series,
        BASE + timedelta(days=effective_day),
        BASE + timedelta(days=available_day),
        1.0, "source", ancestry=("collector",),
        evidence_role="propagation" if series == "g1" else "measurement",
    )


def inspect(rows):
    return audit_directional_lags(
        rows, CUTOFF, [DirectedHypothesis("g1", "industry", 2)]
    )["directional_lags"][0]


def test_same_marginals_have_different_joint_unannounced_leads():
    # Both histories have one apparent lead and one preannounced target.
    # Only the second has an apparent lead BEFORE its target's first release.
    no_unannounced_lead = inspect([
        observation("n0", "g1", 0, 0),
        observation("t2", "industry", 2, -1),
        observation("n3", "g1", 3, 6),
        observation("t5", "industry", 5, 5),
    ])
    one_unannounced_lead = inspect([
        observation("n0", "g1", 0, 0),
        observation("t2", "industry", 2, 2),
        observation("n3", "g1", 3, 6),
        observation("t5", "industry", 5, 1),
    ])
    for report in (no_unannounced_lead, one_unannounced_lead):
        assert report["observed_pair_count"] == 2
        assert report["source_available_before_target_count"] == 1
        assert report["target_preannounced_pair_count"] == 1
    assert no_unannounced_lead["source_available_before_target_and_first_release_count"] == 0
    assert one_unannounced_lead["source_available_before_target_and_first_release_count"] == 1


def test_source_after_physical_target_is_not_an_unannounced_lead():
    report = inspect([
        observation("narrative", "g1", 0, 3),
        observation("shock", "industry", 2, 5),
    ])
    assert report["source_available_before_target_first_release_count"] == 1
    assert report["source_available_before_target_count"] == 0
    assert report["source_available_before_target_and_first_release_count"] == 0


def test_public_announcement_before_source_excludes_apparent_early_warning():
    report = inspect([
        observation("narrative", "g1", 0, 1),
        observation("announced-shock", "industry", 2, 0),
    ])
    assert report["source_available_before_target_count"] == 1
    assert report["target_preannounced_pair_count"] == 1
    assert report["source_available_before_target_and_first_release_count"] == 0
    assert report["predictive_input"] is False
