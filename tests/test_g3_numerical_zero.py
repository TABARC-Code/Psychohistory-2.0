"""Connectedness must not be inferred from an underflowed eigenvalue."""

import numpy as np

from psychohistory.g3.spectral import laplacian_metrics


def _path_graph(n, weight):
    adjacency = np.zeros((n, n))
    for i in range(n - 1):
        adjacency[i, i + 1] = weight
        adjacency[i + 1, i] = weight
    return adjacency


def test_connected_subnormal_path_withholds_numerical_zero():
    adjacency = _path_graph(13, np.nextafter(0.0, 1.0))
    result = laplacian_metrics(adjacency)
    assert result["component_count"] == 1
    assert result["lambda2"] is None
    assert result["lambda2_reliability"] == "UNRESOLVED_NUMERICAL_ZERO"
    assert result["fragmentation_warning"] is False


def test_disconnected_subnormal_path_retains_exact_topological_zero():
    adjacency = _path_graph(13, np.nextafter(0.0, 1.0))
    adjacency[6, 7] = adjacency[7, 6] = 0.0
    result = laplacian_metrics(adjacency)
    assert result["component_count"] == 2
    assert result["lambda2"] == 0.0
    assert result["lambda2_reliability"] == "EXACT_TOPOLOGICAL_ZERO"
    assert result["fragmentation_warning"] is True


def test_ordinary_connected_path_preserves_positive_eigenvalue():
    result = laplacian_metrics(_path_graph(13, 1.0))
    assert result["component_count"] == 1
    assert result["lambda2"] > 0
    assert result["lambda2_reliability"] == "UNCHECKED_NODE_LIMIT"
