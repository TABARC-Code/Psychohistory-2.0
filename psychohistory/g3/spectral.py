"""Undirected non-negative graph Laplacian diagnostics."""
import numpy as np
from fractions import Fraction

from .spectral_bounds import connectivity_interval


def laplacian_metrics(adjacency):
    try:
        A = np.asarray(adjacency, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("numeric adjacency required") from exc
    if (A.ndim != 2 or A.shape[0] == 0 or A.shape[0] != A.shape[1]
            or not np.all(np.isfinite(A))):
        raise ValueError("finite nonempty square adjacency required")
    if (np.any(A < 0) or not np.allclose(A, A.T, rtol=1e-10, atol=0)
            or np.any(np.diag(A) != 0)):
        raise ValueError("symmetric nonnegative adjacency without self-loops required")

    # Fragmentation is topological; an absolute eigenvalue cutoff mislabels
    # connected networks when every edge weight is uniformly small.
    n = len(A)
    seen = np.zeros(n, dtype=bool)
    components = 0
    for start in range(n):
        if seen[start]:
            continue
        components += 1
        seen[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbour in np.flatnonzero(A[node] > 0):
                if not seen[neighbour]:
                    seen[neighbour] = True
                    stack.append(int(neighbour))

    # Preserve exact symmetry before averaging approximately symmetric measurements.
    original_exact_symmetry = np.array_equal(A, A.T)
    # Average tolerated asymmetry without losing subnormal symmetric weights.
    A = A + 0.5 * (A.T - A)
    with np.errstate(over="ignore", invalid="ignore"):
        L = np.diag(A.sum(axis=1)) - A
    if not np.all(np.isfinite(L)):
        raise ValueError("adjacency weights overflow Laplacian construction")
    vals = np.sort(np.linalg.eigvalsh(L))
    if not np.all(np.isfinite(vals)):
        raise ValueError("nonfinite Laplacian eigenvalues")
    vals = np.maximum(vals, 0.0)
    # Topology determines the exact number of zero Laplacian modes.
    # Do not use an absolute eigenvalue threshold: it can erase weak links.
    vals[:components] = 0.0
    lambda2 = float(vals[1]) if n > 1 else None
    reliability = "NOT_APPLICABLE" if n == 1 else "UNCHECKED"
    interval = None
    # Exact-input Rayleigh bounds are necessary checks, not certificates of
    # numerical accuracy or real-world measurement validity.
    if n > 1 and components > 1:
        reliability = "EXACT_TOPOLOGICAL_ZERO"
    elif n > 12:
        reliability = "UNCHECKED_NODE_LIMIT"
    elif not original_exact_symmetry:
        reliability = "UNCHECKED_SYMMETRY_ROUNDING"
    elif n > 1:
        bounds = connectivity_interval(A.tolist())
        lower, upper = bounds["lower"], bounds["upper"]
        interval = {"lower_exact": str(lower), "upper_exact": str(upper)}
        estimate = Fraction.from_float(lambda2)
        # Comparison slack is not a graph-connectivity threshold.
        slack = Fraction(1, 100_000_000)
        if estimate < lower * (1 - slack) or estimate > upper * (1 + slack):
            lambda2 = None
            reliability = "OUTSIDE_PROVEN_BOUNDS"
        else:
            reliability = "WITHIN_BOUNDS_NOT_CERTIFIED"
    return {
        "lambda1": float(vals[0]),
        "lambda2": lambda2,
        "lambda2_reliability": reliability,
        "lambda2_exact_input_bounds": interval,
        "component_count": components,
        "fragmentation_warning": components > 1,
    }
