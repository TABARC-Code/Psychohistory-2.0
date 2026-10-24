"""G3 adjacency measurements must survive binary64 conversion unchanged."""

import numpy as np
import pytest

from psychohistory.g3.spectral import laplacian_metrics
from psychohistory.g3.spectral_bounds import connectivity_interval


def test_unrepresentable_integer_edge_must_not_change_weight():
    graph = np.array([[0, 2**53 + 1], [2**53 + 1, 0]], dtype=object)
    with pytest.raises(ValueError, match="real numeric adjacency required"):
        laplacian_metrics(graph)


def test_extended_precision_edge_must_not_disappear():
    tiny = np.longdouble("1e-4000")
    if tiny <= 0:
        pytest.skip("extended precision not available on this platform")
    graph = np.array([[0, tiny], [tiny, 0]], dtype=np.longdouble)
    with pytest.raises(ValueError, match="real numeric adjacency required"):
        laplacian_metrics(graph)


def test_invalid_boolean_edge_is_not_a_measured_weight():
    with pytest.raises(ValueError, match="real numeric adjacency required"):
        laplacian_metrics([[0, True], [True, 0]])


def test_exact_real_object_array_preserves_connectivity():
    graph = np.array([[0, np.float32(0.25)], [np.float32(0.25), 0]], dtype=object)
    result = laplacian_metrics(graph)
    assert result["component_count"] == 1
    assert result["lambda2"] == pytest.approx(0.5)
    assert result["fragmentation_warning"] is False


def test_exactly_representable_large_integer_is_conservatively_rejected():
    graph = [[0, 2**53 + 2], [2**53 + 2, 0]]
    with pytest.raises(ValueError, match="real numeric adjacency required"):
        laplacian_metrics(graph)


def test_direct_exact_bounds_reject_lossy_integer_edge():
    graph = [[0, 2**53 + 1], [2**53 + 1, 0]]
    with pytest.raises(ValueError, match="numeric weights required"):
        connectivity_interval(graph)


def test_direct_exact_bounds_reject_erased_extended_precision_edge():
    tiny = np.longdouble("1e-4000")
    if tiny <= 0:
        pytest.skip("extended precision not available on this platform")
    graph = np.array([[0, tiny], [tiny, 0]], dtype=np.longdouble)
    with pytest.raises(ValueError, match="numeric weights required"):
        connectivity_interval(graph)
