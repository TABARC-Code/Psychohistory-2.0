"""G1 propagation persistence must measure elapsed instants, not local clock labels."""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.g1.memetics import analyse_memetic_observations
from psychohistory.pipeline import evaluate


def _event(index, when):
    return Observation(
        f"m{index}", "g1:meme", when, when, 1.0, "social",
        evidence_role="propagation", content_ancestry=("root",),
        community_id=f"community-{index}",
    )


def _span(instants):
    observations = [_event(i, instant) for i, instant in enumerate(instants)]
    result = analyse_memetic_observations(observations)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["predictive_input"] is False
    return result["social_resonance"]["persistence_span_seconds"]


def test_autumn_clock_change_counts_repeated_hour():
    london = ZoneInfo("Europe/London")
    before = datetime(2026, 10, 25, 0, 30, tzinfo=london)
    after = datetime(2026, 10, 25, 2, 30, tzinfo=london)
    assert _span([before, after]) == 3 * 3600


def test_spring_clock_change_does_not_count_missing_hour():
    london = ZoneInfo("Europe/London")
    before = datetime(2026, 3, 29, 0, 30, tzinfo=london)
    after = datetime(2026, 3, 29, 2, 30, tzinfo=london)
    assert _span([before, after]) == 3600


def test_fold_reverses_wall_clock_order_without_reversing_time():
    london = ZoneInfo("Europe/London")
    first = datetime(2026, 10, 25, 1, 50, tzinfo=london, fold=0)
    second = datetime(2026, 10, 25, 1, 10, tzinfo=london, fold=1)
    assert _span([first, second]) == 20 * 60
    assert _span([second, first]) == 20 * 60
    assert _span([first.astimezone(UTC), second.astimezone(UTC)]) == 20 * 60


def test_direct_g1_and_sqlite_pipeline_agree_across_clock_change(tmp_path):
    london = ZoneInfo("Europe/London")
    before = datetime(2026, 10, 25, 0, 30, tzinfo=london)
    after = datetime(2026, 10, 25, 2, 30, tzinfo=london)
    observations = [_event(0, before), _event(1, after)]
    store = Store(tmp_path / "events.db")
    for observation in observations:
        store.add_observation(observation)
    as_of = datetime(2026, 10, 25, 3, 0, tzinfo=london)
    result = evaluate(store, as_of)
    assert result["g1_measurement"]["valid"]
    assert result["g1_memetics"]["social_resonance"]["persistence_span_seconds"] == 10800
    assert _span([before, after]) == 10800


def test_invalid_direct_g1_clock_fails_closed():
    invalid = datetime(2026, 10, 25, 0, 30)
    result = analyse_memetic_observations([_event(0, invalid)])
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
    assert "timestamp" in result["reason"]
