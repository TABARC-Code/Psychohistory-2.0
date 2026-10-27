"""G1 pooled view counts must not silently lose unit increments.

All per-video counts can be binary64-safe while their floating-point sum
is not. A diagnostic candidate must not imply that rounded aggregate
velocity is a verified discrete count.
"""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 27, 0, tzinfo=UTC)


def _pair(video, growth, *, topic="industrial"):
    start = CUTOFF - timedelta(hours=2)
    end = CUTOFF - timedelta(hours=1)
    base = {
        "video_id": video,
        "creator_id": "creator-" + video,
        "topic": topic,
        "format": "short",
        "published_at": CUTOFF - timedelta(days=1),
    }
    return [
        {**base, "observed_at": start, "available_at": start, "views": 0},
        {**base, "observed_at": end, "available_at": end, "views": growth},
    ]


def test_pooled_binary64_safe_counts_cannot_hide_lost_unit_increments():
    rows = [row for video, growth in (
        ("large", 2**53), ("small1", 1), ("small2", 1)
    ) for row in _pair(video, growth)]
    series = analyse_video_trends(rows, CUTOFF)["series"][0]
    assert series["paired_creator_count_unverified"] == 3
    assert series["growing_paired_creator_count_unverified"] == 3
    assert series["unsafe_view_count_video_count"] == 0
    assert series["view_delta_exact_integer"] == str(2**53 + 2)
    assert series["numerical_integrity_status"] == "UNRESOLVED_AGGREGATE_COUNT_GRANULARITY"
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_unsafe_pooled_count_does_not_poison_independent_small_topic():
    rows = [row for video, growth in (
        ("large", 2**53), ("small1", 1), ("small2", 1)
    ) for row in _pair(video, growth)]
    rows += [row for i in range(3) for row in _pair(f"healthy{i}", 10, topic="health")]
    series = {item["topic"]: item for item in analyse_video_trends(rows, CUTOFF)["series"]}
    assert series["industrial"]["status"] == "UNRESOLVED"
    assert series["health"]["view_delta_exact_integer"] == "30"
    assert series["health"]["numerical_integrity_status"] == "VALID"
    assert series["health"]["status"] == "CANDIDATE_NOT_ADMITTED"


def test_unsafe_source_counter_cannot_claim_exact_aggregate_audit():
    # Large binary64 counters are already withheld, but their difference
    # is not necessarily the true difference between integer view counts.
    rows = []
    for video in ("large1", "large2", "large3"):
        start = CUTOFF - timedelta(hours=2)
        end = CUTOFF - timedelta(hours=1)
        base = {
            "video_id": video, "creator_id": "creator-" + video,
            "topic": "hardware", "format": "short",
            "published_at": CUTOFF - timedelta(days=1),
        }
        rows.extend([
            {**base, "observed_at": start, "available_at": start,
             "views": float(2**53 + 2)},
            {**base, "observed_at": end, "available_at": end,
             "views": float(2**53 + 4)},
        ])
    series = analyse_video_trends(rows, CUTOFF)["series"][0]
    assert series["unsafe_view_count_video_count"] == 3
    assert series["view_delta_exact_integer"] is None
    assert series["numerical_integrity_status"] == "UNRESOLVED_COUNT_GRANULARITY"
    assert series["status"] == "UNRESOLVED"
