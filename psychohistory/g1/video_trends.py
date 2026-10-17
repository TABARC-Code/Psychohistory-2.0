"""Conservative, exposure-aware video and meme trend diagnostics.

Public counts cannot identify recommendation algorithms or causal transmission.
Every output is a non-admitted candidate until independently validated.
"""
from collections import defaultdict
from datetime import UTC, datetime
from math import isfinite, log1p


def _utc(value):
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware datetimes")
    return value.astimezone(UTC)


def analyse_video_trends(observations, as_of, *, min_creators=3):
    """Analyse point-in-time video snapshots.

    Each record is a dict containing video_id, creator_id, published_at,
    observed_at, views, topic, format ('short' or 'long'), and optional
    lineage_id, community_id, exposure and available_at. Snapshots are cumulative.
    View velocity uses only successive snapshots for the SAME video.
    """
    cutoff = _utc(as_of)
    grouped = defaultdict(list)
    validated = []
    identities = {}
    conflicting_videos = set()
    rejected = 0
    for record in observations:
        try:
            published = _utc(record["published_at"])
            observed = _utc(record["observed_at"])
            if published > observed or observed > cutoff:
                continue
            # Observation and first-availability times are distinct.
            availability = record.get("available_at")
            if availability is not None:
                available = _utc(availability)
                if available < observed:
                    raise ValueError("snapshot available before observation")
                if available > cutoff:
                    continue
            views = record["views"]
            exposure = record.get("exposure")
            if isinstance(views, bool) or not isinstance(views, (int, float)) or not isfinite(views) or views < 0:
                raise ValueError("invalid views")
            if exposure is not None and (isinstance(exposure, bool) or not isinstance(exposure, (int, float)) or not isfinite(exposure) or exposure <= 0):
                raise ValueError("invalid exposure")
            if record["format"] not in ("short", "long"):
                raise ValueError("invalid format")
            if not all(isinstance(record[k], str) and record[k] for k in ("video_id", "creator_id", "topic")):
                raise ValueError("invalid identifiers")
            identity = (record["creator_id"], record["topic"],
                        record["format"], published)
            video_id = record["video_id"]
            if video_id in identities and identities[video_id] != identity:
                conflicting_videos.add(video_id)
            else:
                identities[video_id] = identity
            validated.append((observed, views, record))
        except (KeyError, TypeError, ValueError, OverflowError):
            rejected += 1
    rejected += len(conflicting_videos)
    for observed, views, record in validated:
        if record["video_id"] not in conflicting_videos:
            grouped[(record["topic"], record["format"], record["video_id"])].append(
                (observed, views, record))
    topics = defaultdict(lambda: {
        "creator_ids": set(), "paired_creator_ids": set(),
        "community_ids": set(), "lineage_ids": set(),
        "videos": 0, "view_delta": 0.0, "hours": 0.0,
        "exposure_view_delta": 0.0, "exposure_delta": 0.0,
        "exposure_pairs": 0, "paired": 0,
        "snapshots": 0, "available_snapshots": 0})
    for (topic, fmt, _), snapshots in grouped.items():
        snapshots.sort(key=lambda x: x[0])
        # A timestamp collision is ambiguous; exclude it from velocity estimation.
        if len({s[0] for s in snapshots}) != len(snapshots):
            rejected += 1
            continue
        last = snapshots[-1][2]
        key = (topic, fmt)
        entry = topics[key]
        entry["videos"] += 1
        entry["snapshots"] += len(snapshots)
        entry["available_snapshots"] += sum(
            snapshot[2].get("available_at") is not None
            for snapshot in snapshots
        )
        entry["creator_ids"].add(last["creator_id"])
        if last.get("community_id"):
            entry["community_ids"].add(last["community_id"])
        if last.get("lineage_id"):
            entry["lineage_ids"].add(last["lineage_id"])
        if len(snapshots) >= 2:
            before, after = snapshots[-2:]
            delta = after[1] - before[1]
            hours = (after[0] - before[0]).total_seconds() / 3600
            if not isfinite(delta) or delta < 0 or not isfinite(hours) or hours <= 0:
                rejected += 1
                continue
            entry["view_delta"] += delta
            entry["hours"] += hours
            entry["paired"] += 1
            entry["paired_creator_ids"].add(last["creator_id"])
            e0, e1 = before[2].get("exposure"), after[2].get("exposure")
            if e0 is not None and e1 is not None and e1 > e0:
                exposure_delta = e1 - e0
                if isfinite(exposure_delta):
                    entry["exposure_delta"] += exposure_delta
                    entry["exposure_view_delta"] += delta
                    entry["exposure_pairs"] += 1
    result = []
    for (topic, fmt), entry in sorted(topics.items()):
        creators = len(entry["creator_ids"])
        velocity = entry["view_delta"] / entry["hours"] if entry["hours"] else None
        exposure_rate = (entry["exposure_view_delta"] / entry["exposure_delta"]
                         if entry["exposure_delta"] > 0 else None)
        result.append({
            "topic": topic, "format": fmt, "video_count": entry["videos"],
            "independent_creator_count_unverified": creators,
            "paired_creator_count_unverified": len(entry["paired_creator_ids"]),
            "snapshot_availability_coverage_fraction": (
                entry["available_snapshots"] / entry["snapshots"]
                if entry["snapshots"] else 0.0
            ),
            "snapshot_availability_status": (
                "REPORTED_COMPLETE" if entry["available_snapshots"] == entry["snapshots"]
                else "PARTIAL" if entry["available_snapshots"]
                else "UNMEASURED"
            ),
            "exposure_pair_coverage_fraction": (
                entry["exposure_pairs"] / entry["paired"] if entry["paired"] else 0.0
            ),
            "community_breadth": len(entry["community_ids"]),
            "observed_lineage_breadth": len(entry["lineage_ids"]),
            "view_velocity_per_video_hour": velocity,
            "exposure_adjusted_view_rate": exposure_rate,
            "log_view_delta": log1p(entry["view_delta"]),
            "status": "CANDIDATE_NOT_ADMITTED" if (
                len(entry["paired_creator_ids"]) >= min_creators and entry["paired"]
            ) else "UNRESOLVED",
            "predictive_input": False,
            "algorithmic_amplification": "NOT_IDENTIFIABLE_FROM_PUBLIC_COUNTS",
        })
    return {"status": "DIAGNOSTIC_ONLY", "predictive_input": False,
            "rejected_records": rejected, "series": result}
