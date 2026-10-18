from collections import defaultdict
from math import isfinite
from numbers import Real


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
    obs = list(obs)
    errors = []
    warnings = []
    seen = set()
    measurement_ancestry = defaultdict(int)
    content_ancestry = defaultdict(int)
    propagation = []

    for o in obs:
        if o.available_at > as_of:
            errors.append(f"future leakage: {o.observation_id}")
        if o.observation_id in seen:
            errors.append(f"duplicate id: {o.observation_id}")
        seen.add(o.observation_id)
        if (isinstance(o.value, bool) or not isinstance(o.value, Real)
                or not isfinite(o.value)):
            errors.append(f"invalid numeric value: {o.observation_id}")
        if (isinstance(o.quality, bool) or not isinstance(o.quality, Real)
                or not isfinite(o.quality) or not 0 <= o.quality <= 1):
            errors.append(f"invalid quality: {o.observation_id}")
        if o.revision_type not in {
            "none", "scheduled_revision", "maturation",
            "methodological_revision", "correction"
        }:
            warnings.append(f"unknown revision type: {o.observation_id}")

        if o.is_propagation:
            propagation.append(o)
            for ancestor in o.content_ancestry:
                content_ancestry[ancestor] += 1
        else:
            for ancestor in o.ancestry:
                measurement_ancestry[ancestor] += 1

    measurement_breadth, shared_measurement = _component_breadth(
        [o for o in obs if not o.is_propagation], lambda o: o.ancestry
    )
    propagation_measurement_breadth, shared_propagation_measurement = _component_breadth(
        propagation, lambda o: o.ancestry
    )
    content_breadth, shared_content = _component_breadth(
        propagation, lambda o: o.content_ancestry
    )

    observed_content = [o for o in propagation if o.content_ancestry]
    observed_content_breadth, _ = _component_breadth(
        observed_content, lambda o: o.content_ancestry
    )
    content_coverage = (
        len(observed_content) / len(propagation) if propagation else 0.0
    )

    # A shared measurement ancestor can affect both a shock observation and
    # a propagation observation; it is not evidence of content transmission.
    ordinary = [o for o in obs if not o.is_propagation]
    ordinary_sources = defaultdict(int)
    propagation_sources = defaultdict(int)
    for event in ordinary:
        for ancestor in set(event.ancestry):
            ordinary_sources[ancestor] += 1
    for event in propagation:
        for ancestor in set(event.ancestry):
            propagation_sources[ancestor] += 1
    cross_role_shared = {
        ancestor: {
            "measurement_events": ordinary_sources[ancestor],
            "propagation_events": propagation_sources[ancestor],
        }
        for ancestor in sorted(ordinary_sources.keys() & propagation_sources.keys())
    }
    ordinary_coverage = (
        sum(bool(o.ancestry) for o in ordinary) / len(ordinary)
        if ordinary else 0.0
    )
    propagation_coverage = (
        sum(bool(o.ancestry) for o in propagation) / len(propagation)
        if propagation else 0.0
    )
    if cross_role_shared:
        cross_role_status = "OBSERVED_SHARED"
    elif not ordinary or not propagation:
        cross_role_status = "NOT_APPLICABLE"
    elif ordinary_coverage < 1 or propagation_coverage < 1:
        cross_role_status = "PARTIAL_UNMEASURED"
    else:
        cross_role_status = "NO_SHARED_OBSERVED"

    carriers = {o.carrier for o in propagation if o.carrier}
    actors = {o.actor_id for o in propagation if o.actor_id}
    communities = {o.community_id for o in propagation if o.community_id}
    variants = {o.semantic_variant for o in propagation if o.semantic_variant}

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "shared_measurement_ancestry": shared_measurement,
        "shared_cross_role_measurement_ancestry": cross_role_shared,
        "cross_role_measurement_ancestry_status": cross_role_status,
        "measurement_ancestry_coverage_fraction": ordinary_coverage,
        "propagation_measurement_ancestry_coverage_fraction": propagation_coverage,
        "measurement_informational_breadth_upper_bound": measurement_breadth,
        "shared_content_ancestry": shared_content,
        "shared_propagation_measurement_ancestry": shared_propagation_measurement,
        "propagation_measurement_breadth_upper_bound": propagation_measurement_breadth,
        "content_origin_breadth_upper_bound": content_breadth,
        "content_origin_observed_components": observed_content_breadth,
        "content_ancestry_coverage_fraction": content_coverage,
        "content_ancestry_unknown_events": len(propagation) - len(observed_content),
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
        "informational_breadth_upper_bound": measurement_breadth,
    }
