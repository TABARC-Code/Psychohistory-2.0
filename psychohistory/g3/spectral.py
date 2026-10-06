import numpy as np


def laplacian_metrics(adjacency):
    A = np.asarray(adjacency, float)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or not np.allclose(A, A.T):
        raise ValueError("undirected symmetric adjacency required")
    L = np.diag(A.sum(axis=1)) - A
    vals = np.linalg.eigvalsh(L)
    vals = np.sort(vals)
    return {
        "lambda1": float(vals[0]),
        "lambda2": float(vals[1]) if len(vals) > 1 else None,
        "fragmentation_warning": bool(len(vals) > 1 and vals[1] < 1e-8),
    }
