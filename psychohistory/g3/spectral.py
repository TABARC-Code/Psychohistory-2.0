import numpy as np


def laplacian_metrics(adjacency):
    matrix = np.asarray(adjacency, float)
    if (
        matrix.ndim != 2
        or matrix.shape[0] != matrix.shape[1]
        or not np.allclose(matrix, matrix.T)
    ):
        raise ValueError("undirected symmetric adjacency required")
    laplacian = np.diag(matrix.sum(axis=1)) - matrix
    values = np.sort(np.linalg.eigvalsh(laplacian))
    return {
        "lambda1": float(values[0]),
        "lambda2": float(values[1]) if len(values) > 1 else None,
        "fragmentation_warning": bool(len(values) > 1 and values[1] < 1e-8),
    }
