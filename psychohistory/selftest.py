import json

from .g1.hawkes import fit_exponential_hawkes
from .g2.ou import fit_ou
from .g3.spectral import laplacian_metrics
from .g23.gate import coupling_gate
from .validation.scoring import brier


def run():
    # SYNTHETIC/DETERMINISTIC VERIFICATION ONLY. Never enter these results in
    # the empirical forecast ledger or report them as predictive validation.
    results = {
        "label": "SYNTHETIC_VERIFICATION_NOT_EMPIRICAL_VALIDATION",
        "g1_hawkes": fit_exponential_hawkes(
            [0.2, 0.5, 0.9, 1.0, 1.15, 1.8, 2.5, 3.7], 4.0
        ),
        "g2_ou": fit_ou(
            range(10), [1.0, 0.81, 0.67, 0.59, 0.48, 0.43, 0.39, 0.36, 0.34, 0.33]
        ),
        "g3_connected": laplacian_metrics(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        ),
        "g3_fragmented": laplacian_metrics(
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
        ),
        "g23_weak_evidence": coupling_gate(
            out_of_sample_gain=0.1,
            valid_null=False,
            identifiable=False,
            multiplicity_corrected=False,
        ),
        "scoring_known_example": brier(
            [("a", 0.2, 0.4, 0), ("b", 0.8, 0.6, 1)]
        ),
    }
    return results


def main():
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()
