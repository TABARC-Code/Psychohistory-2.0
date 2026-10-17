from fractions import Fraction

import numpy as np

from psychohistory.g3.spectral import laplacian_metrics


def test_weak_bridge_upper_bound_violation_is_unresolved():
    A = [[0, 1, 0], [1, 0, 1e-20], [0, 1e-20, 0]]
    result = laplacian_metrics(A)
    assert result["component_count"] == 1
    assert result["lambda2"] is None
    assert result["lambda2_reliability"] == "OUTSIDE_PROVEN_BOUNDS"
    assert Fraction(result["lambda2_exact_input_bounds"]["upper_exact"]) == (
        3 * Fraction.from_float(1e-20) / 2
    )


def test_small_connected_graph_stays_numeric():
    result = laplacian_metrics([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert result["lambda2"] > 0
    assert result["lambda2_reliability"] == "WITHIN_BOUNDS_NOT_CERTIFIED"


def test_disconnected_topology_exact_zero():
    result = laplacian_metrics([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    assert result["lambda2"] == 0
    assert result["lambda2_reliability"] == "EXACT_TOPOLOGICAL_ZERO"


def test_single_node_not_applicable():
    result = laplacian_metrics([[0]])
    assert result["lambda2"] is None
    assert result["lambda2_reliability"] == "NOT_APPLICABLE"


def test_larger_graph_does_not_claim_certification():
    A = np.ones((13, 13)) - np.eye(13)
    result = laplacian_metrics(A)
    assert result["lambda2_reliability"] == "UNCHECKED_NODE_LIMIT"


def test_weak_edge_never_promoted_to_zero_topology():
    A = [[0, 1, 0], [1, 0, 1e-40], [0, 1e-40, 0]]
    result = laplacian_metrics(A)
    assert result["component_count"] == 1
    assert result["fragmentation_warning"] is False
    assert result["lambda2_reliability"] in {
        "OUTSIDE_PROVEN_BOUNDS", "WITHIN_BOUNDS_NOT_CERTIFIED"
    }
