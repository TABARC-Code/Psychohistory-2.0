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
    # Collection-source ancestry and copied-content ancestry are distinct.
    known_lineages = [set(o.content_ancestry) for o in events]
    known_count = sum(bool(lineage) for lineage in known_lineages)
    lineages = defaultdict(int)
    lineage_communities = defaultdict(set)
    for event, lineage in zip(events, known_lineages):
        for ancestor in lineage:
            lineages[ancestor] += 1
            if event.community_id:
                lineage_communities[ancestor].add(event.community_id)

    shared = {ancestor for ancestor, count in lineages.items() if count > 1}
    shared_events = sum(bool(lineage & shared) for lineage in known_lineages)
    lineage_coverage = known_count / len(events)
    shared_lineage_fraction = shared_events / len(events) if known_count == len(events) else None
    cross_lineages = {
        ancestor for ancestor, labels in lineage_communities.items() if len(labels) > 1
    }
    cross_events = sum(
        bool(lineage & cross_lineages) and bool(event.community_id)
        for event, lineage in zip(events, known_lineages)
    )
    community_coverage = sum(bool(o.community_id) for o in events) / len(events)
    cross_complete = known_count == len(events) and community_coverage == 1
    # Lineage overlap is descriptive, not a causal transmission estimate.
    known_variants = sum(bool(o.semantic_variant) for o in events)
    missing_variants = len(events) - known_variants
    variant_richness_ratio = len(variants) / len(events) if not missing_variants else None
    cross_community_breadth = len(communities)
    carrier_breadth = len(carriers)

    # These are behavioural diagnostics, not measurements of endorsement or
    # a collective subconscious. They require external validation before use
    # as predictive features.
    resonance = {
        "event_count": len(events),
        "endogenous_reproduction_fraction": None,
        "endogenous_reproduction_status": "UNMEASURED",
        "shared_lineage_event_fraction": shared_lineage_fraction,
        "shared_lineage_observed_lower_bound": shared_events / len(events),
        "content_lineage_coverage": lineage_coverage,
        "cross_community_lineage_event_fraction": (
            cross_events / len(events) if cross_complete else None
        ),
        "cross_community_lineage_observed_lower_bound": cross_events / len(events),
        "community_label_coverage": community_coverage,
        "cross_community_lineage_count": len(cross_lineages),
        "cross_community_interpretation": (
            "observed shared content, not directional transmission or causation"
        ),
        "semantic_variant_ratio": variant_richness_ratio,
        "semantic_variant_observed_lower_bound": len(variants) / len(events),
        "semantic_variant_possible_upper_bound": (
            len(variants) + missing_variants
        ) / len(events),
        "semantic_variant_coverage": known_variants / len(events),
        "semantic_variant_interpretation": (
            "distinct labelled variants per event, not a mutation rate"
        ),
        "community_breadth": cross_community_breadth,
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
            "events_with_known_content_lineage": known_count,
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
