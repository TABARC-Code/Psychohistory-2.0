"""Point-in-time short-video spikes and independent meme-watch diagnostics.

The output is descriptive, not an inference about YouTube's recommender or
population behaviour. Admission requires independent rolling-origin validation.
"""
from collections import defaultdict
from datetime import datetime, timezone
from math import isfinite, log1p
from statistics import median


def _instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("timezone-aware datetime required")
    return value.astimezone(timezone.utc)


def analyse_topic_spikes(windows, as_of, *, baseline_windows=4, ratio_threshold=3.0):
    """Detect short-form topic bursts against earlier, exposure-adjusted windows.

    Windows must contain topic, start, end, views_delta, video_count, creator_count,
    and optionally exposure_delta. No missing exposure is silently imputed.
    Each topic's windows must be non-overlapping. Last window is compared only
    with earlier windows; no future or contemporaneous baseline leakage.
    """
    cutoff = _instant(as_of)
    groups = defaultdict(list)
    rejected = 0
    for w in windows:
        try:
            start, end = _instant(w["start"]), _instant(w["end"])
            if end > cutoff:
                continue
            if end <= start:
                raise ValueError("invalid interval")
            topic = w["topic"]
            if not isinstance(topic, str) or not topic:
                raise ValueError("invalid topic")
            for field in ("views_delta", "video_count", "creator_count"):
                value = w[field]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
                    raise ValueError("invalid count")
            exposure = w.get("exposure_delta")
            if exposure is not None and (isinstance(exposure, bool) or not isinstance(exposure, (int, float)) or not isfinite(exposure) or exposure <= 0):
                raise ValueError("invalid exposure")
            groups[topic].append((start, end, w))
        except (KeyError, TypeError, ValueError, OverflowError):
            rejected += 1
    output = []
    for topic, entries in sorted(groups.items()):
        entries.sort(key=lambda x: x[0])
        if any(a[1] > b[0] for a, b in zip(entries, entries[1:])):
            rejected += 1
            continue
        if len(entries) < baseline_windows + 1:
            output.append({"topic": topic, "status": "INSUFFICIENT_HISTORY", "predictive_input": False})
            continue
        prior = [e[2] for e in entries[-baseline_windows-1:-1]]
        current = entries[-1][2]
        exposure_ready = all(x.get("exposure_delta") is not None for x in prior + [current])
        def rate(w):
            return w["views_delta"] / w["exposure_delta"] if exposure_ready else w["views_delta"] / ((_instant(w["end"]) - _instant(w["start"])).total_seconds() / 3600)
        baseline = median(rate(x) for x in prior)
        now = rate(current)
        ratio = now / baseline if baseline > 0 else None
        output.append({
            "topic": topic, "status": "CANDIDATE_NOT_ADMITTED",
            "rate_basis": "views_per_exposure" if exposure_ready else "views_per_hour_UNADJUSTED",
            "baseline_median": baseline, "current_rate": now,
            "spike_ratio": ratio, "spike_detected": ratio is not None and ratio >= ratio_threshold,
            "creator_count_reported": current["creator_count"],
            "video_count": current["video_count"],
            "algorithmic_amplification": "UNIDENTIFIED",
            "population_shift": "UNTESTED", "predictive_input": False,
        })
    return {"status": "DIAGNOSTIC_ONLY", "rejected_windows": rejected,
            "predictive_input": False, "topics": output}


def analyse_meme_watch(events, as_of):
    """Track distinct observed variants and carriers, not inferred replication."""
    cutoff = _instant(as_of)
    groups = defaultdict(list)
    rejected = 0
    for event in events:
        try:
            observed = _instant(event["observed_at"])
            if observed > cutoff:
                continue
            topic = event["topic"]
            if not isinstance(topic, str) or not topic:
                raise ValueError("invalid topic")
            groups[topic].append(event)
        except (KeyError, ValueError, TypeError):
            rejected += 1
    results = []
    for topic, rows in sorted(groups.items()):
        def distinct(field):
            return len({row[field] for row in rows if isinstance(row.get(field), str) and row[field]})
        results.append({
            "topic": topic, "observations": len(rows),
            "variant_breadth": distinct("semantic_variant"),
            "community_breadth": distinct("community_id"),
            "carrier_breadth": distinct("carrier"),
            "content_ancestry_breadth": distinct("lineage_id"),
            "endogenous_reproduction_fraction": None,
            "transmission": "UNIDENTIFIED",
            "predictive_input": False,
        })
    return {"status": "DIAGNOSTIC_ONLY", "rejected_events": rejected,
            "predictive_input": False, "topics": results}
