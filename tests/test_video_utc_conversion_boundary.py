"""UTC-convertible clock boundary for the G1 video trend sidecar."""

from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.g1.video_trends import analyse_video_trends


NOW = datetime(2026, 10, 24, 8, tzinfo=UTC)


class BrokenOffset(tzinfo):
    def utcoffset(self, dt):
        raise OverflowError("offset provider failed")

    def dst(self, dt):
        return None


def _snapshot(video, observed):
    return {
        "video_id": video, "creator_id": video, "topic": "industrial",
        "format": "short", "published_at": NOW - timedelta(days=1),
        "observed_at": observed, "available_at": observed, "views": 10,
    }


@pytest.mark.parametrize("bad_cutoff", [
    datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
    datetime.max.replace(tzinfo=timezone(-timedelta(hours=1))),
    NOW.replace(tzinfo=BrokenOffset()),
])
def test_unconvertible_cutoff_raises_controlled_validation_error(bad_cutoff):
    with pytest.raises(ValueError, match="timezone-aware"):
        analyse_video_trends([], bad_cutoff)


@pytest.mark.parametrize("field", ["published_at", "observed_at", "available_at"])
def test_unconvertible_snapshot_rejected_without_losing_valid_neighbour(field):
    invalid = _snapshot("bad", NOW - timedelta(hours=2))
    invalid[field] = datetime.min.replace(
        tzinfo=timezone(timedelta(hours=1))
    )
    valid = _snapshot("good", NOW - timedelta(hours=1))
    result = analyse_video_trends([invalid, valid], NOW, min_creators=1)
    assert result["rejected_records"] == 1
    assert len(result["series"]) == 1
    assert result["series"][0]["video_count"] == 1
    assert result["series"][0]["predictive_input"] is False


def test_valid_non_utc_cutoff_preserves_same_observations():
    rows = [_snapshot("good", NOW - timedelta(hours=1))]
    result = analyse_video_trends(
        rows, NOW.astimezone(timezone(timedelta(hours=5))), min_creators=1
    )
    assert result["rejected_records"] == 0
    assert result["series"][0]["video_count"] == 1
    assert result["series"][0]["predictive_input"] is False
