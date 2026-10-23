from collections import Counter, defaultdict
from math import log1p


ATTRIBUTION_HYPOTHESES = (
    "organic_endogenous",
    "domestic_coordinated",
    "foreign_coordinated",
    "common_broadcaster_or_event",
    "algorithmic_amplification",
    "sampling_or_measurement_artifact",
)


def _possible_cross_community_overlap_upper(events):
    """Bound overlap by events with at least one feasible cross-community peer.

    An unknown ancestry can share a root with another event. Two known,
    disjoint ancestries cannot. Unknown community labels may differ from
    any observed label. This is a necessary-pair bound, not a claim that
    all potential pairings jointly occurred or establish transmission.
    """
    community_counts = Counter(event.community_id for event in events)
    unknown_ancestry_communities = Counter(
        event.community_id for event in events if not event.content_ancestry
    )
    unknown_ancestry_total = sum(unknown_ancestry_communities.values())
    root_communities = defaultdict(Counter)
    for event in events:
        for root in set(event.content_ancestry):
            root_communities[root][event.community_id] += 1

    possible = 0
    for event in events:
        community = event.community_id
        if not event.content_ancestry:
            # The event can adopt any root, but still needs a different
            # possible community somewhere else in the observed population.
            has_peer = (
                len(events) > 1 if not community
                else len(events) > community_counts[community]
            )
        else:
            # A missing-ancestry peer could adopt one of this event's roots.
            has_peer = (
                unknown_ancestry_total > 0 if not community
                else unknown_ancestry_total > unknown_ancestry_communities[community]
            )
            if not has_peer:
                for root in set(event.content_ancestry):
                    members = root_communities[root]
                    # Exclude known peers in the same community. Unknown
                    # labels can always be assigned to a distinct community.
                    if (sum(members.values()) > 1 if not community
                            else sum(members.values()) > members[community]):
                        has_peer = True
                        break
        possible += bool(has_peer)
    return possible / len(events)


def analyse_memetic_observations(observations):
    events = [o for o in observations if o.is_propagation]
    if not events:
        return {
            "status": "UNRESOLVED",
            "reason": "no memetic propagation observations",
            "predictive_input": False,
        }

    carriers = Counter(o.carrier for o in events if o.carrier)
    actors = Counter(o.actor_id for o in events if o.actor_id)
    communities = Counter(o.community_id for o in events if o.community_id)
    variants = Counter(o.semantic_variant for o in events if o.semantic_variant)
    lineages = defaultdict(int)
    for event in events:
        for ancestor in set(event.content_ancestry):
            lineages[ancestor] += 1

    shared = {ancestor for ancestor, count in lineages.items() if count > 1}
    shared_events = sum(
        bool(set(event.content_ancestry) & shared)
        for event in events
    )
    shared_lineage_fraction = shared_events / len(events)
    lineage_observed = sum(bool(event.content_ancestry) for event in events)
    lineage_coverage = lineage_observed / len(events)
    lineage_upper_bound = (
        1.0 if lineage_observed < len(events) and len(events) > 1
        else shared_lineage_fraction
    )
    lineage_status = (
        "MEASURED" if lineage_observed == len(events) else
        "PARTIAL" if lineage_observed else "UNMEASURED"
    )
    # Lineage overlap alone cannot identify endogenous reproduction.
    mutation_ratio = len(variants) / len(events) if variants else 0.0
    # Unlabelled observations can conceal variants and communities.
    labelled_variants = sum(bool(o.semantic_variant) for o in events)
    missing_variants = len(events) - labelled_variants
    mutation_ratio_upper_bound = (len(variants) + missing_variants) / len(events)
    mutation_ratio_observed = (
        len(variants) / labelled_variants if labelled_variants else None
    )
    labelled_communities = sum(bool(o.community_id) for o in events)
    missing_communities = len(events) - labelled_communities
    cross_community_breadth = len(communities)
    # Community breadth alone is not evidence of inter-community transmission.
    # Link observed content ancestors to observed communities, without
    # conflating source/collector ancestry with content ancestry.
    lineage_communities = defaultdict(set)
    for event in events:
        if event.community_id:
            for ancestor in set(event.content_ancestry):
                lineage_communities[ancestor].add(event.community_id)
    cross_community_lineages = {
        ancestor for ancestor, members in lineage_communities.items()
        if len(members) >= 2
    }
    cross_community_overlap_events = sum(
        bool(event.community_id and
             set(event.content_ancestry) & cross_community_lineages)
        for event in events
    )
    complete_joint_metadata = all(
        event.community_id and event.content_ancestry for event in events
    )
    # When every community label is known and all events belong to one
    # community, missing content ancestry cannot conceal cross-community
    # overlap. A universal upper bound of one would be mathematically loose.
    single_known_community = (
        missing_communities == 0 and cross_community_breadth <= 1
    )
    cross_community_overlap_lower = cross_community_overlap_events / len(events)
    if complete_joint_metadata or len(events) == 1 or single_known_community:
        cross_community_overlap_upper = cross_community_overlap_lower
    elif lineage_observed == len(events):
        # Complete content ancestry limits possible overlap to lineages seen
        # on at least two events. An unknown community may be distinct from
        # every observed community, but cannot invent a missing content root.
        possible_cross_lineages = {
            ancestor for ancestor, count in lineages.items()
            if count > 1 and (
                len(lineage_communities[ancestor]) >= 2
                or any(
                    not event.community_id and ancestor in event.content_ancestry
                    for event in events
                )
            )
        }
        cross_community_overlap_upper = sum(
            bool(set(event.content_ancestry) & possible_cross_lineages)
            for event in events
        ) / len(events)
    else:
        # Missing roots can be assigned freely, but a known-root event
        # cannot overlap a disjoint known root without a feasible peer in
        # a different community. Preserve a conservative upper bound.
        cross_community_overlap_upper = _possible_cross_community_overlap_upper(
            events
        )
    carrier_breadth = len(carriers)

    # These are behavioural diagnostics, not measurements of endorsement or
    # a collective subconscious. They require external validation before use
    # as predictive features.
    resonance = {
        "event_count": len(events),
        "endogenous_reproduction_fraction": None,
        "endogenous_reproduction_status": "UNMEASURED",
        # With incomplete ancestry coverage this is an observed lower bound,
        # not proof of independent origins or transmission.
        "shared_lineage_event_fraction": shared_lineage_fraction,
        "shared_lineage_event_fraction_lower_bound": shared_lineage_fraction,
        "shared_lineage_event_fraction_upper_bound": lineage_upper_bound,
        "shared_lineage_fraction_status": lineage_status,
        "content_ancestry_coverage_fraction": lineage_coverage,
        "semantic_variant_ratio": mutation_ratio,
        "semantic_variant_ratio_lower_bound": mutation_ratio,
        "semantic_variant_ratio_upper_bound": mutation_ratio_upper_bound,
        "semantic_variant_ratio_observed": mutation_ratio_observed,
        "semantic_variant_coverage_fraction": labelled_variants / len(events),
        "community_coverage_fraction": labelled_communities / len(events),
        "community_breadth_lower_bound": cross_community_breadth,
        "community_breadth_upper_bound": cross_community_breadth + missing_communities,
        "community_breadth": cross_community_breadth,
        "cross_community_content_lineages_observed": len(cross_community_lineages),
        "cross_community_lineage_overlap_event_fraction_lower_bound": (
            cross_community_overlap_lower
        ),
        "cross_community_lineage_overlap_event_fraction_upper_bound": (
            cross_community_overlap_upper
        ),
        "cross_community_lineage_overlap_status": (
            "MEASURED" if complete_joint_metadata else
            "PARTIAL" if any(o.community_id and o.content_ancestry for o in events)
            else "UNMEASURED"
        ),
        "carrier_breadth": carrier_breadth,
        "persistence_span_seconds": (
            max(o.effective_at for o in events) - min(o.effective_at for o in events)
        ).total_seconds() if len(events) > 1 else 0.0,
        "log_event_volume": log1p(len(events)),
    }

    return {
        "status": "CANDIDATE_NOT_ADMITTED",
        "predictive_input": False,
        "propagation": {
            "events": len(events),
            "carriers": dict(carriers),
            "actors_observed": len(actors),
            "communities_observed": len(communities),
            "content_lineages": len(lineages),
        },
        "social_resonance": resonance,
        "coordination": {
            "status": "UNRESOLVED",
            "reason": "requires synchrony/topology null model; volume alone is insufficient",
        },
        "attribution": {
            "status": "UNRESOLVED",
            "hypotheses": list(ATTRIBUTION_HYPOTHESES),
            "reason": "coordination is not attribution; no actor is inferred from propagation alone",
        },
        "interpretation_guard": (
            "social resonance is latent behavioural inference; repetition does not "
            "mechanically imply endorsement and does not directly measure subconscious state"
        ),
    }
