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
    lineages = defaultdict(int)
    for event in events:
        for ancestor in event.content_ancestry or event.ancestry:
            lineages[ancestor] += 1

    repeated = sum(v - 1 for v in lineages.values() if v > 1)
    endogenous_reproduction = repeated / len(events)
    mutation_ratio = len(variants) / len(events) if variants else 0.0
    cross_community_breadth = len(communities)
    carrier_breadth = len(carriers)

    # These are behavioural diagnostics, not measurements of endorsement or
    # a collective subconscious. They require external validation before use
    # as predictive features.
    resonance = {
        "event_count": len(events),
        "endogenous_reproduction_fraction": endogenous_reproduction,
        "semantic_variant_ratio": mutation_ratio,
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
