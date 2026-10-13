"""Undirected non-negative graph Laplacian diagnostics."""
import numpy as np


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

    L = np.diag(A.sum(axis=1)) - A
    vals = np.sort(np.linalg.eigvalsh(L))
    return {
        "lambda1": float(vals[0]),
        "lambda2": float(vals[1]) if n > 1 else None,
        "component_count": components,
        "fragmentation_warning": components > 1,
    }
