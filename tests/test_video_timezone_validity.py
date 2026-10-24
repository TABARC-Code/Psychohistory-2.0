"""Reject timezone objects that do not establish a UTC offset."""
from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.g1.video_trends import analyse_video_trends


class UnknownOffset(tzinfo):
    def utcoffset(self, dt):
        return None

    def dst(self, dt):
        return None

    def tzname(self, dt):
        return "unknown"


NOW = datetime(2026, 10, 24, 3, tzinfo=UTC)
UNKNOWN = UnknownOffset()


def snapshot(video, observed, *, published=None, available=None):
    return {
        "video_id": video,
        "creator_id": video,
        "topic": "industrial",
        "format": "short",
        "published_at": published or NOW - timedelta(days=1),
        "observed_at": observed,
        "available_at": available if available is not None else observed,
        "views": 10,
    }


def test_unknown_offset_cutoff_is_not_localised_implicitly():
    cutoff = NOW.replace(tzinfo=UNKNOWN)
    with pytest.raises(ValueError, match="timezone-aware"):
        analyse_video_trends([], cutoff)


@pytest.mark.parametrize("field", ["published_at", "observed_at", "available_at"])
def test_unknown_offset_record_is_rejected_without_poisoning_valid_neighbour(field):
    invalid = snapshot("bad", NOW - timedelta(hours=2))
    invalid[field] = invalid[field].replace(tzinfo=UNKNOWN)
    valid = snapshot("good", NOW - timedelta(hours=1))
    result = analyse_video_trends([invalid, valid], NOW, min_creators=1)
    assert result["rejected_records"] == 1
    assert len(result["series"]) == 1
    assert result["series"][0]["video_count"] == 1
    assert result["series"][0]["predictive_input"] is False


def test_valid_non_utc_offset_remains_supported():
    offset = timezone(timedelta(hours=2))
    rows = [
        snapshot("v", (NOW - timedelta(hours=2)).astimezone(offset)),
        snapshot("v", (NOW - timedelta(hours=1)).astimezone(offset)),
    ]
    rows[1]["views"] = 20
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 0
    assert result["series"][0]["view_velocity_per_video_hour"] == 10
    assert result["series"][0]["predictive_input"] is False
