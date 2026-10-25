"""Propagation diagnostics require events to have occurred before observation.

A scheduled future event is not measured propagation, even if its planned
details were published earlier. Compare absolute UTC instants, not local
wall-clock fields, and keep diagnostic admission closed.
"""

from datetime import UTC, datetime, timedelta, timezone

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


WHEN = datetime(2026, 10, 25, 10, tzinfo=UTC)


def event(name, *, effective_at=WHEN, available_at=WHEN):
    return Observation(
        observation_id=name,
        series="g1:industrial_disruption",
        effective_at=effective_at,
        available_at=available_at,
        value=1.0,
        source="first_observation",
        evidence_role="propagation",
        ancestry=("independent-collector",),
        content_ancestry=("shared-industrial-origin",),
        community_id=name,
    )


def test_direct_g1_rejects_future_event_known_from_advance_notice():
    rows = [
        event("actual"),
        event("planned", effective_at=WHEN + timedelta(days=2)),
    ]
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert "chronology" in result["reason"]
    assert result["predictive_input"] is False


def test_direct_g1_rejects_cross_offset_advance_notice():
    ahead = timezone(timedelta(hours=5, minutes=30))
    rows = [
        event("actual"),
        event(
            "planned",
            effective_at=(WHEN + timedelta(hours=1)).astimezone(ahead),
            available_at=WHEN.astimezone(timezone(timedelta(hours=-4))),
        ),
    ]
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


def test_direct_g1_accepts_same_absolute_instant_with_different_offsets():
    ahead = timezone(timedelta(hours=5, minutes=30))
    rows = [
        event("first"),
        event("second", available_at=WHEN.astimezone(ahead)),
    ]
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["social_resonance"]["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1.0
    assert result["predictive_input"] is False


def test_direct_g1_accepts_late_observation_of_completed_event():
    rows = [
        event("first"),
        event("second", available_at=WHEN + timedelta(days=1)),
    ]
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["social_resonance"]["shared_lineage_event_fraction_lower_bound"] == 1.0
    assert result["predictive_input"] is False
