from collections import defaultdict


def _collapsed_breadth(total, ancestry):
    dependent = {k: v for k, v in ancestry.items() if v > 1}
    return max(0, total - sum(v - 1 for v in dependent.values())), dependent


def validate_observations(obs, as_of):
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
        if not 0 <= o.quality <= 1:
            errors.append(f"invalid quality: {o.observation_id}")
        if o.revision_type not in {
            "none", "scheduled_revision", "maturation",
            "methodological_revision", "correction"
        }:
            warnings.append(f"unknown revision type: {o.observation_id}")

        if o.is_propagation:
            propagation.append(o)
            for ancestor in o.content_ancestry or o.ancestry:
                content_ancestry[ancestor] += 1
        else:
            for ancestor in o.ancestry:
                measurement_ancestry[ancestor] += 1

    ordinary = len(obs) - len(propagation)
    measurement_breadth, shared_measurement = _collapsed_breadth(
        ordinary, measurement_ancestry
    )
    content_breadth, shared_content = _collapsed_breadth(
        len(propagation), content_ancestry
    )

    carriers = {o.carrier for o in propagation if o.carrier}
    actors = {o.actor_id for o in propagation if o.actor_id}
    communities = {o.community_id for o in propagation if o.community_id}
    variants = {o.semantic_variant for o in propagation if o.semantic_variant}

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "shared_measurement_ancestry": shared_measurement,
        "measurement_informational_breadth_upper_bound": measurement_breadth,
        "shared_content_ancestry": shared_content,
        "content_origin_breadth_upper_bound": content_breadth,
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
