from collections import defaultdict
from datetime import datetime
from math import isfinite
from numbers import Real


def _finite_real(value):
    return not isinstance(value, bool) and isinstance(value, Real) and isfinite(value)


def _aware_instant(value):
    return isinstance(value, datetime) and value.tzinfo is not None and value.utcoffset() is not None


def _collapsed_breadth(total, ancestry):
    """Legacy count-only estimate; not suitable for overlapping ancestry sets."""
    dependent = {k: v for k, v in ancestry.items() if v > 1}
    return max(0, total - sum(v - 1 for v in dependent.values())), dependent


def _component_breadth(observations, lineage_attribute):
    """Count connected evidence groups; shared ancestors join observations.

    This is a structural upper bound, not proof of statistical independence.
    """
    parents = list(range(len(observations)))
    owners = {}
    counts = defaultdict(int)

    def root(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    for i, observation in enumerate(observations):
        for ancestor in set(lineage_attribute(observation)):
            counts[ancestor] += 1
            if ancestor in owners:
                parents[root(i)] = root(owners[ancestor])
            else:
                owners[ancestor] = i
    return len({root(i) for i in range(len(observations))}), {
        key: count for key, count in counts.items() if count > 1
    }


def validate_observations(obs, as_of):
    if not _aware_instant(as_of):
        raise ValueError("as_of must be a timezone-aware datetime")
    errors = []
    warnings = []
    seen = set()
    propagation = []

    for o in obs:
        if not _aware_instant(o.available_at) or not _aware_instant(o.effective_at):
            errors.append(f"invalid timestamp: {o.observation_id}")
        elif o.available_at > as_of:
            errors.append(f"future leakage: {o.observation_id}")
        if o.observation_id in seen:
            errors.append(f"duplicate id: {o.observation_id}")
        seen.add(o.observation_id)
        if not _finite_real(o.quality) or not 0 <= o.quality <= 1:
            errors.append(f"invalid quality: {o.observation_id}")
        if not _finite_real(o.value):
            errors.append(f"invalid value: {o.observation_id}")
        if o.revision_type not in {
            "none", "scheduled_revision", "maturation",
            "methodological_revision", "correction"
        }:
            warnings.append(f"unknown revision type: {o.observation_id}")

        if o.is_propagation:
            propagation.append(o)

    measurement = [o for o in obs if not o.is_propagation]
    known_measurement = [o for o in measurement if o.ancestry]
    measurement_breadth, shared_measurement = _component_breadth(
        known_measurement, lambda o: o.ancestry
    )
    measurement_complete = len(known_measurement) == len(measurement)
    if not measurement_complete:
        warnings.append("measurement ancestry missing; evidence independence unresolved")
    known_content = [o for o in propagation if o.content_ancestry]
    content_breadth, shared_content = _component_breadth(
        known_content, lambda o: o.content_ancestry
    )
    content_complete = len(known_content) == len(propagation)
    if not content_complete:
        warnings.append("content ancestry missing; content-origin independence unresolved")

    carriers = {o.carrier for o in propagation if o.carrier}
    actors = {o.actor_id for o in propagation if o.actor_id}
    communities = {o.community_id for o in propagation if o.community_id}
    variants = {o.semantic_variant for o in propagation if o.semantic_variant}

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "shared_measurement_ancestry": shared_measurement,
        "measurement_informational_breadth_upper_bound": (
            measurement_breadth if measurement_complete else None
        ),
        "measurement_breadth_known_subset": measurement_breadth,
        "measurement_ancestry_coverage": (
            len(known_measurement) / len(measurement) if measurement else None
        ),
        "measurement_breadth_status": (
            "BOUNDED" if measurement_complete else "UNRESOLVED"
        ),
        "shared_content_ancestry": shared_content,
        "content_origin_breadth_upper_bound": (
            content_breadth if content_complete else None
        ),
        "content_origin_breadth_known_subset": content_breadth,
        "content_ancestry_coverage": (
            len(known_content) / len(propagation) if propagation else None
        ),
        "content_origin_breadth_status": (
            "BOUNDED" if content_complete else "UNRESOLVED"
        ),
        "propagation_event_count": len(propagation),
        "carrier_breadth": len(carriers),
        "actor_breadth": len(actors),
        "community_breadth": len(communities),
        "semantic_variant_breadth": len(variants),
        "claim_relative_rule": (
            "shared content ancestry reduces independence for content/origin/"
            "attribution claims but does not erase distinct propagation events"
        ),
        # Compatibility: this remains the conservative breadth for ordinary
        # measurement evidence and must not be used to deduplicate G1 propagation.
        "informational_breadth_upper_bound": (
            measurement_breadth if measurement_complete else None
        ),
    }
