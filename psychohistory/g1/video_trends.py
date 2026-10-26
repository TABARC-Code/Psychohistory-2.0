"""Conservative, exposure-aware video and meme trend diagnostics.

Public counts cannot identify recommendation algorithms or causal transmission.
Every output is a non-admitted candidate until independently validated.
"""
from collections import defaultdict
from datetime import UTC
from itertools import pairwise
from math import isfinite, log1p

from ..core.numeric_precision import exact_binary64_real
from ..core.validation import _aware_instant, _valid_optional_label


def _utc(value):
    # A defined offset is not enough: conversion itself can overflow the
    # representable datetime range or fail in a custom timezone provider.
    if not _aware_instant(value):
        raise ValueError("timestamps must be timezone-aware datetimes convertible to UTC")
    return value.astimezone(UTC)


def analyse_video_trends(observations, as_of, *, min_creators=3):
    """Analyse point-in-time video snapshots.

    Each record is a dict containing video_id, creator_id, published_at,
    observed_at, views, topic, format ('short' or 'long'), and optional
    lineage_id, community_id, exposure and available_at. Snapshots are cumulative.
    View velocity uses only successive snapshots for the SAME video.
    """
    # Creator breadth is an integer count, not a tunable floating threshold.
    # Reject zero, negative and Boolean settings before measuring candidates.
    if type(min_creators) is not int or min_creators < 1:
        raise ValueError("min_creators must be a positive integer")
    cutoff = _utc(as_of)
    grouped = defaultdict(list)
    validated = []
    identities = {}
    stable_metadata = {}
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
            # View counts are discrete. Beyond 2**53, even exactly
            # representable floats cannot resolve every single-view change.
            # Match the existing conservative large-integer boundary rather
            # than allowing floating-point input to bypass it.
            if not exact_binary64_real(views) or views < 0 or views > 2**53:
                raise ValueError("invalid views")
            if exposure is not None and (
                    not exact_binary64_real(exposure) or exposure < 0):
                raise ValueError("invalid exposure")
            # NumPy scalars pass the same exact-value check as Python numbers.
            # Convert only afterwards so the pooled rates stay binary64.
            views = float(views)
            # View totals are discrete observations, even when a provider
            # serialises them as floats. Fractional totals manufacture growth.
            # Exposure remains a measured denominator and may be fractional.
            if not views.is_integer():
                raise ValueError("fractional cumulative view count")
            exposure = float(exposure) if exposure is not None else None
            record = {**record, "views": views, "exposure": exposure}
            if record["format"] not in ("short", "long"):
                raise ValueError("invalid format")
            if not all(
                type(record[k]) is str and record[k].strip()
                and record[k] == record[k].strip()
                for k in ("video_id", "creator_id", "topic")
            ):
                raise ValueError("invalid identifiers")
            # Optional labels identify content ancestry and community breadth.
            # They must remain stable for a video across snapshots.
            for field in ("community_id", "lineage_id"):
                label = record.get(field)
                # Padded labels are distinct strings but not distinct measured
                # communities or content roots. Reject rather than silently
                # normalise identifiers and obscure the original evidence.
                if (not _valid_optional_label(label)
                        or (label is not None and label != label.strip())):
                    raise ValueError("invalid optional identifier")
            identity = (record["creator_id"], record["topic"],
                        record["format"], published)
            video_id = record["video_id"]
            if video_id in identities and identities[video_id] != identity:
                conflicting_videos.add(video_id)
            else:
                identities[video_id] = identity
            labels = stable_metadata.setdefault(video_id, {})
            for field in ("community_id", "lineage_id"):
                value = record.get(field)
                if value:
                    if field in labels and labels[field] != value:
                        conflicting_videos.add(video_id)
                    else:
                        labels[field] = value
            validated.append((observed, views, record))
        except (KeyError, TypeError, ValueError, OverflowError):
            rejected += 1
    rejected += sum(1 for _, _, record in validated
                    if record["video_id"] in conflicting_videos)
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
        "snapshots": 0, "available_snapshots": 0,
        "availability_adjacent_pairs": 0, "availability_reported_pairs": 0,
        "inverted_availability_pairs": 0,
        "exposure_snapshots": 0, "exposure_rollback_video_count": 0})
    for (topic, fmt, _), snapshots in grouped.items():
        snapshots.sort(key=lambda x: x[0])
        # A timestamp collision is ambiguous; exclude it from velocity estimation.
        if len({s[0] for s in snapshots}) != len(snapshots):
            rejected += len(snapshots)
            continue
        # Views are cumulative over the visible history. A later recovery
        # does not repair an earlier count rollback. Exclude the whole video
        # before adding community, lineage or creator breadth, rather than
        # allowing inconsistent telemetry to imply narrative transmission.
        if any(
            later[1] < earlier[1] or not isfinite(later[1] - earlier[1])
            for earlier, later in pairwise(snapshots)
        ):
            rejected += len(snapshots)
            continue
        # Counts are cumulative over the entire visible history. An earlier
        # rollback is not repaired by an increase in the final pair. Compare
        # consecutive known measurements even across missing snapshots.
        exposure_history = [
            snapshot[2]["exposure"] for snapshot in snapshots
            if snapshot[2].get("exposure") is not None
        ]
        exposure_rollback = any(
            later < earlier or not isfinite(later - earlier)
            for earlier, later in pairwise(exposure_history)
        )
        last = snapshots[-1][2]
        key = (topic, fmt)
        entry = topics[key]
        # A later ordered pair cannot repair an earlier inversion in the
        # reported first-availability chronology. Keep retrospective rates
        # separate from point-in-time eligibility.
        entry["availability_adjacent_pairs"] += max(0, len(snapshots) - 1)
        # Coverage counts directly adjacent observed snapshots. Chronological
        # integrity instead compares successive *reported* availability times,
        # including across gaps in optional metadata. A missing middle record
        # must not conceal a known inversion between its neighbours.
        reported_availability = [
            _utc(snapshot[2]["available_at"]) for snapshot in snapshots
            if snapshot[2].get("available_at") is not None
        ]
        entry["availability_reported_pairs"] += sum(
            earlier[2].get("available_at") is not None
            and later[2].get("available_at") is not None
            for earlier, later in pairwise(snapshots)
        )
        entry["inverted_availability_pairs"] += sum(
            first > second for first, second in pairwise(reported_availability)
        )
        entry["exposure_snapshots"] += len(exposure_history)
        entry["exposure_rollback_video_count"] += int(exposure_rollback)
        entry["videos"] += 1
        entry["snapshots"] += len(snapshots)
        entry["available_snapshots"] += sum(
            snapshot[2].get("available_at") is not None
            for snapshot in snapshots
        )
        entry["creator_ids"].add(last["creator_id"])
        # Missing labels in a later snapshot do not erase known ancestry.
        labels = stable_metadata[last["video_id"]]
        if labels.get("community_id"):
            entry["community_ids"].add(labels["community_id"])
        if labels.get("lineage_id"):
            entry["lineage_ids"].add(labels["lineage_id"])
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
            if (not exposure_rollback and e0 is not None and e1 is not None
                    and e1 > e0):
                exposure_delta = e1 - e0
                if isfinite(exposure_delta):
                    entry["exposure_delta"] += exposure_delta
                    entry["exposure_view_delta"] += delta
                    entry["exposure_pairs"] += 1
    result = []
    for (topic, fmt), entry in sorted(topics.items()):
        creators = len(entry["creator_ids"])
        # Individually finite cumulative count changes can overflow when
        # aggregated across many videos. A finite numerator divided by a very
        # short observation interval can also overflow. Never publish inf,
        # NaN or a false zero exposure rate as a usable candidate.
        totals_finite = all(isfinite(entry[key]) for key in (
            "view_delta", "hours", "exposure_view_delta", "exposure_delta"
        ))
        velocity = (
            entry["view_delta"] / entry["hours"]
            if isfinite(entry["view_delta"]) and isfinite(entry["hours"])
            and entry["hours"] > 0 else None
        )
        if velocity is not None and not isfinite(velocity):
            velocity = None
        exposure_rate = (
            entry["exposure_view_delta"] / entry["exposure_delta"]
            if isfinite(entry["exposure_view_delta"])
            and isfinite(entry["exposure_delta"])
            and entry["exposure_delta"] > 0 else None
        )
        if exposure_rate is not None and not isfinite(exposure_rate):
            exposure_rate = None
        numeric_ok = (
            totals_finite
            and (entry["hours"] == 0 or velocity is not None)
            and (entry["exposure_delta"] == 0 or exposure_rate is not None)
        )
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
            "availability_history_pair_coverage_fraction": (
                entry["availability_reported_pairs"] / entry["availability_adjacent_pairs"]
                if entry["availability_adjacent_pairs"] else 0.0
            ),
            "out_of_order_availability_pair_count": entry["inverted_availability_pairs"],
            "point_in_time_velocity_status": (
                "UNRESOLVED_AVAILABILITY_ORDER" if entry["inverted_availability_pairs"]
                else "REPORTED_ONLY_UNVERIFIED" if entry["availability_adjacent_pairs"]
                and entry["availability_reported_pairs"] == entry["availability_adjacent_pairs"]
                and entry["available_snapshots"] == entry["snapshots"]
                else "UNVERIFIED_AVAILABILITY"
            ),
            "exposure_pair_coverage_fraction": (
                entry["exposure_pairs"] / entry["paired"] if entry["paired"] else 0.0
            ),
            "exposure_rollback_video_count": entry["exposure_rollback_video_count"],
            "exposure_history_status": (
                "CUMULATIVE_ROLLBACK" if entry["exposure_rollback_video_count"]
                else "UNMEASURED" if not entry["exposure_snapshots"]
                else "PARTIAL" if entry["exposure_snapshots"] < entry["snapshots"]
                else "MONOTONE_REPORTED"
            ),
            "community_breadth": len(entry["community_ids"]),
            "observed_lineage_breadth": len(entry["lineage_ids"]),
            "view_velocity_per_video_hour": velocity,
            "exposure_adjusted_view_rate": exposure_rate,
            "log_view_delta": (log1p(entry["view_delta"])
                               if isfinite(entry["view_delta"]) else None),
            "numerical_integrity_status": (
                "VALID" if numeric_ok else "UNRESOLVED_AGGREGATE_OVERFLOW"
            ),
            "status": "CANDIDATE_NOT_ADMITTED" if (
                numeric_ok and not entry["exposure_rollback_video_count"]
                and not entry["inverted_availability_pairs"]
                # Retrospective velocity alone cannot establish when counts
                # first became available to a point-in-time observer.
                and entry["available_snapshots"] == entry["snapshots"]
                and entry["availability_adjacent_pairs"] > 0
                and entry["availability_reported_pairs"] == entry["availability_adjacent_pairs"]
                and len(entry["paired_creator_ids"]) >= min_creators and entry["paired"]
            ) else "UNRESOLVED",
            "predictive_input": False,
            "algorithmic_amplification": "NOT_IDENTIFIABLE_FROM_PUBLIC_COUNTS",
        })
    return {"status": "DIAGNOSTIC_ONLY", "predictive_input": False,
            "rejected_records": rejected, "series": result}
