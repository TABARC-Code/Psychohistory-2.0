"""Undirected non-negative graph Laplacian diagnostics.

Fragmentation is a topological property, not an absolute eigenvalue cutoff.
"""
import numpy as np


def laplacian_metrics(adjacency):
    A = np.asarray(adjacency, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or A.shape[0] == 0:
        raise ValueError("nonempty square adjacency required")
    if not np.all(np.isfinite(A)) or np.any(A < 0):
        raise ValueError("finite nonnegative adjacency required")
    if not np.allclose(A, A.T, rtol=1e-12, atol=0):
        raise ValueError("undirected symmetric adjacency required")
    if np.any(np.diag(A) != 0):
        raise ValueError("self-loops require a separate graph model")
    A = (A + A.T) / 2
    degree = A.sum(axis=1)
    if not np.all(np.isfinite(degree)):
        raise ValueError("nonfinite graph degree")

    # Count components from the support graph. Scaling weights cannot change
    # whether a positive-weight edge exists.
    unseen = set(range(len(A)))
    components = 0
    while unseen:
        components += 1
        pending = [unseen.pop()]
        while pending:
            node = pending.pop()
            neighbours = set(np.flatnonzero(A[node] > 0)) & unseen
            pending.extend(neighbours)
            unseen.difference_update(neighbours)

    L = np.diag(degree) - A
    if not np.all(np.isfinite(L)):
        raise ValueError("nonfinite Laplacian")
    vals = np.linalg.eigvalsh(L)
    # Symmetric normalised Laplacian is invariant to a global positive
    # rescaling of edge weights. Isolated vertices have a zero row/column.
    inverse_sqrt = np.divide(
        1.0, np.sqrt(degree), out=np.zeros_like(degree), where=degree > 0
    )
    normalised_L = (inverse_sqrt[:, None] * L) * inverse_sqrt[None, :]
    normalised_vals = np.linalg.eigvalsh(normalised_L)
    if not np.all(np.isfinite(normalised_vals)):
        raise ValueError("nonfinite normalised Laplacian spectrum")
    if not np.all(np.isfinite(vals)):
        raise ValueError("nonfinite Laplacian spectrum")
    return {
        "lambda1": float(vals[0]),
        "lambda2": float(vals[1]) if len(vals) > 1 else None,
        "lambda2_normalised": float(normalised_vals[1]) if len(vals) > 1 else None,
        "connected_components": components,
        "fragmentation_warning": components > 1,
    }
