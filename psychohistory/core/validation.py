from collections import defaultdict
from datetime import UTC, datetime
from .numeric_precision import exact_binary64_real


def _finite_real(value):
    """Check original finite measurements without binary64 rounding."""
    return exact_binary64_real(value)


def _aware_instant(value):
    """Reject naive clocks and timezone objects without a defined offset."""
    if not isinstance(value, datetime) or value.tzinfo is None:
        return False
    try:
        if value.utcoffset() is None:
            return False
        # A defined offset is insufficient if conversion crosses datetime's
        # representable bounds. Validate the actual UTC instant.
        value.astimezone(UTC)
        return True
    except (TypeError, ValueError, OverflowError):
        return False


def _valid_ancestry(value):
    """Require canonical source IDs without silently normalising evidence.

    A padded root and its unpadded spelling must not become two independent
    measurement sources or content origins. Empty collections remain unknown.
    """
    return (isinstance(value, (tuple, list))
            and all(type(token) is str and bool(token.strip())
                    and token == token.strip() for token in value))


def _valid_primary_label(value):
    """Reject ambiguous primary identities rather than rewriting provenance."""
    return type(value) is str and bool(value.strip()) and value == value.strip()


def _valid_optional_label(value):
    """Optional evidence IDs must be canonical text or genuinely unrecorded.

    Padded labels can split one observed community, actor or content variant
    into apparently independent identities. Reject rather than rewrite them.
    """
    return value is None or (
        type(value) is str and bool(value.strip()) and value == value.strip()
    )


def _safe_ancestry(value):
    return tuple(value) if _valid_ancestry(value) else ()


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
    cutoff = as_of.astimezone(UTC)
    obs = list(obs)
    errors = []
    warnings = []
    seen = set()
    measurement_ancestry = defaultdict(int)
    content_ancestry = defaultdict(int)
    propagation = []

    for o in obs:
        if not _aware_instant(o.available_at):
            errors.append(f"invalid availability timestamp: {o.observation_id}")
        elif o.available_at.astimezone(UTC) > cutoff:
            errors.append(f"future leakage: {o.observation_id}")
        if not _aware_instant(o.effective_at):
            errors.append(f"invalid effective timestamp: {o.observation_id}")
        # Future-effective G1 candidates are excluded by the pipeline at
        # this cutoff. Do not let a scheduled event invalidate current G1;
        # once effective, its first-availability must not predate occurrence.
        # Ordinary measurements may legitimately describe future shocks.
        if (o.is_propagation and _aware_instant(o.effective_at)
                and _aware_instant(o.available_at)
                and o.effective_at.astimezone(UTC) <= cutoff
                and o.effective_at.astimezone(UTC) > o.available_at.astimezone(UTC)):
            errors.append(f"propagation chronology: {o.observation_id}")
        identifier = o.observation_id
        if not _valid_primary_label(identifier):
            # Avoid hashing malformed or unhashable identifiers.
            errors.append(f"invalid observation_id: {identifier!r}")
        else:
            if identifier in seen:
                errors.append(f"duplicate id: {identifier}")
            seen.add(identifier)
        if hasattr(o, "series") and (
                not _valid_primary_label(o.series)):
            errors.append(f"invalid series: {identifier!r}")
        # Historical SQL NULL source/vintage is unrecorded. Reject explicit
        # malformed labels, without inventing provenance for old records.
        for field in ("source", "vintage"):
            if hasattr(o, field):
                label = getattr(o, field)
                if label is not None and (
                        not _valid_primary_label(label)):
                    errors.append(f"invalid {field}: {identifier!r}")
        # A whitespace-only community is not a second observed community.
        # Reject malformed labels before G1 breadth and overlap diagnostics.
        for field in (
            "pipeline_position", "carrier", "actor_id",
            "community_id", "semantic_variant",
        ):
            if hasattr(o, field) and not _valid_optional_label(getattr(o, field)):
                errors.append(f"invalid {field}: {identifier!r}")
        if not _finite_real(o.value):
            errors.append(f"invalid numeric value: {o.observation_id}")
        if not _finite_real(o.quality) or not 0 <= o.quality <= 1:
            errors.append(f"invalid quality: {o.observation_id}")
        if hasattr(o, "evidence_role") and (
                type(o.evidence_role) is not str or
                o.evidence_role not in ("measurement", "propagation")):
            errors.append(f"invalid evidence role: {o.observation_id}")
        # Unknown textual revisions retain the legacy warning. Non-text
        # metadata is invalid evidence, and unhashable objects must not
        # crash the point-in-time validator.
        if type(o.revision_type) is not str:
            errors.append(f"invalid revision type: {o.observation_id}")
        elif o.revision_type not in {
            "none", "scheduled_revision", "maturation",
            "methodological_revision", "correction"
        }:
            warnings.append(f"unknown revision type: {o.observation_id}")
        if not _valid_ancestry(o.ancestry):
            errors.append(f"invalid measurement ancestry: {o.observation_id}")
        if not _valid_ancestry(o.content_ancestry):
            errors.append(f"invalid content ancestry: {o.observation_id}")

        if o.is_propagation:
            propagation.append(o)
            for ancestor in _safe_ancestry(o.content_ancestry):
                content_ancestry[ancestor] += 1
        else:
            for ancestor in _safe_ancestry(o.ancestry):
                measurement_ancestry[ancestor] += 1

    measurement_breadth, shared_measurement = _component_breadth(
        [o for o in obs if not o.is_propagation], lambda o: _safe_ancestry(o.ancestry)
    )
    propagation_measurement_breadth, shared_propagation_measurement = _component_breadth(
        propagation, lambda o: _safe_ancestry(o.ancestry)
    )
    content_breadth, shared_content = _component_breadth(
        propagation, lambda o: _safe_ancestry(o.content_ancestry)
    )

    observed_content = [o for o in propagation if _safe_ancestry(o.content_ancestry)]
    observed_content_breadth, _ = _component_breadth(
        observed_content, lambda o: _safe_ancestry(o.content_ancestry)
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
        for ancestor in set(_safe_ancestry(event.ancestry)):
            ordinary_sources[ancestor] += 1
    for event in propagation:
        for ancestor in set(_safe_ancestry(event.ancestry)):
            propagation_sources[ancestor] += 1
    cross_role_shared = {
        ancestor: {
            "measurement_events": ordinary_sources[ancestor],
            "propagation_events": propagation_sources[ancestor],
        }
        for ancestor in sorted(ordinary_sources.keys() & propagation_sources.keys())
    }
    ordinary_coverage = (
        sum(bool(_safe_ancestry(o.ancestry)) for o in ordinary) / len(ordinary)
        if ordinary else 0.0
    )
    propagation_coverage = (
        sum(bool(_safe_ancestry(o.ancestry)) for o in propagation) / len(propagation)
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

    # Invalid optional labels have already been recorded as errors above.
    # Do not hash malformed containers while assembling diagnostic breadth:
    # a bad observation should fail validation, not crash the entire batch.
    carriers = {
        o.carrier for o in propagation
        if _valid_optional_label(o.carrier) and o.carrier
    }
    actors = {
        o.actor_id for o in propagation
        if _valid_optional_label(o.actor_id) and o.actor_id
    }
    communities = {
        o.community_id for o in propagation
        if _valid_optional_label(o.community_id) and o.community_id
    }
    variants = {
        o.semantic_variant for o in propagation
        if _valid_optional_label(o.semantic_variant) and o.semantic_variant
    }

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
