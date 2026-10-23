"""Complex adjacency must never be silently projected onto a real network."""

import numpy as np
import pytest

from psychohistory.g3.spectral import laplacian_metrics


@pytest.mark.parametrize("adjacency", [
    np.array([[0, 1 + 2j], [1 - 2j, 0]], dtype=complex),
    [[0, 1 + 2j], [1 - 2j, 0]],
    np.array([[0, 1 + 0j], [1 + 0j, 0]], dtype=complex),
    np.array([[0, complex(1, 0)], [complex(1, 0), 0]], dtype=object),
])
def test_complex_network_measurements_are_rejected(adjacency):
    with pytest.raises(ValueError, match="real numeric adjacency required"):
        laplacian_metrics(adjacency)


def test_real_network_preserves_connectivity_and_eigenvalue():
    result = laplacian_metrics(np.array([[0.0, 2.0], [2.0, 0.0]]))
    assert result["component_count"] == 1
    assert result["lambda2"] == pytest.approx(4.0)
    assert result["fragmentation_warning"] is False


def test_real_object_array_still_supported():
    result = laplacian_metrics(np.array([[0, 1], [1, 0]], dtype=object))
    assert result["component_count"] == 1
    assert result["lambda2"] == pytest.approx(2.0)
