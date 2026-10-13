from datetime import UTC, datetime, timedelta

from psychohistory.g1.topic_watch import analyse_meme_watch, analyse_topic_spikes

T = datetime(2026, 10, 13, tzinfo=UTC)


def row(i, views=10, exposure=None):
    result = {"topic": "software", "start": T + timedelta(hours=i),
              "end": T + timedelta(hours=i + 1), "views_delta": views,
              "video_count": 2, "creator_count": 2}
    if exposure is not None:
        result["exposure_delta"] = exposure
    return result


def test_exposure_rate_removes_distribution_spike():
    windows = [row(i, 10, 100) for i in range(4)]
    windows.append(row(4, 50, 500))
    result = analyse_topic_spikes(windows, T + timedelta(hours=5))
    assert result["topics"][0]["spike_ratio"] == 1
    assert result["topics"][0]["predictive_input"] is False


def test_unadjusted_spike_flagged():
    windows = [row(i, 10 if i < 4 else 50) for i in range(5)]
    result = analyse_topic_spikes(windows, T + timedelta(hours=5))
    assert result["topics"][0]["spike_detected"] is True
    assert result["topics"][0]["rate_basis"] == "views_per_hour_UNADJUSTED"


def test_future_window_excluded():
    result = analyse_topic_spikes([row(i) for i in range(5)],
                                  T + timedelta(hours=4))
    assert result["topics"][0]["status"] == "INSUFFICIENT_HISTORY"


def test_meme_side_watch_not_admitted():
    item = {"topic": "software", "observed_at": T,
            "semantic_variant": "a", "carrier": "short", "community_id": "c"}
    result = analyse_meme_watch([item, dict(item)], T)
    assert result["topics"][0]["variant_breadth"] == 1
    assert result["topics"][0]["endogenous_reproduction_fraction"] is None
    assert result["predictive_input"] is False
