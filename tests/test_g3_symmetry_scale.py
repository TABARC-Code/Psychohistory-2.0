import numpy as np
import pytest

from psychohistory.g3.spectral import laplacian_metrics


def test_near_symmetric_large_weight_no_false_negative_eigenvalue():
    adjacency = [[0, 1e12, 1e12], [1e12 + 50, 0, 1e12], [1e12, 1e12, 0]]
    result = laplacian_metrics(adjacency)
    assert result["lambda1"] == 0
    assert result["lambda2"] > 0
    assert result["component_count"] == 1


def test_exact_symmetric_preserves_algebraic_connectivity():
    rng = np.random.default_rng(131)
    for n in (2, 3, 8, 16):
        for _ in range(100):
            x = rng.uniform(0, 10, (n, n))
            adjacency = np.triu(x, 1)
            adjacency = adjacency + adjacency.T
            expected = np.linalg.eigvalsh(
                np.diag(adjacency.sum(axis=1)) - adjacency
            )[1]
            assert np.isclose(
                laplacian_metrics(adjacency)["lambda2"],
                expected, rtol=1e-12, atol=1e-11
            )


def test_asymmetry_rejected():
    with pytest.raises(ValueError):
        laplacian_metrics([[0, 1], [1.01, 0]])


def test_weight_scale_and_components():
    for scale in (1e-12, 1, 1e12):
        result = laplacian_metrics(np.array([[0, 1], [1, 0]]) * scale)
        assert result["lambda1"] == 0
        assert np.isclose(result["lambda2"], 2 * scale)
        assert result["component_count"] == 1
    disconnected = laplacian_metrics([[0, 0], [0, 0]])
    assert disconnected["component_count"] == 2
    assert disconnected["fragmentation_warning"]


def test_nonfinite_laplacian_rejected():
    with pytest.raises(ValueError, match="overflow"):
        laplacian_metrics(
            [[0, 1e308, 1e308], [1e308, 0, 1e308], [1e308, 1e308, 0]]
        )


def test_subnormal_symmetric_edge_not_erased():
    weight = np.nextafter(0.0, 1.0)
    result = laplacian_metrics([[0.0, weight], [weight, 0.0]])
    assert result["component_count"] == 1
    assert result["lambda2"] > 0.0
