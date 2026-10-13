import pytest

from psychohistory.g1.hawkes import fit_exponential_hawkes
from psychohistory.g3.spectral import laplacian_metrics


def test_tied_events_do_not_claim_identifiable_hawkes():
    result = fit_exponential_hawkes([1, 1, 1, 2, 3, 4], 10)
    assert result["status"] == "UNRESOLVED"
    assert "tied timestamps" in result["reason"]


def test_hawkes_rejects_out_of_window_events():
    assert fit_exponential_hawkes([1, 2, 3, 4, 11], 10)["status"] == "UNRESOLVED"


@pytest.mark.parametrize("scale", [1e-12, 1.0, 1e9])
def test_connected_graph_fragmentation_is_scale_invariant(scale):
    graph = [[0, scale, 0], [scale, 0, scale], [0, scale, 0]]
    result = laplacian_metrics(graph)
    assert result["component_count"] == 1
    assert result["fragmentation_warning"] is False


def test_disconnected_graph_is_fragmented():
    result = laplacian_metrics([[0, 0], [0, 0]])
    assert result["component_count"] == 2
    assert result["fragmentation_warning"] is True


@pytest.mark.parametrize("graph", [
    [], [[0, -1], [-1, 0]], [[0, float("nan")], [float("nan"), 0]],
    [[0, 1], [0, 0]], [[1]],
])
def test_invalid_adjacency_is_rejected(graph):
    with pytest.raises(ValueError):
        laplacian_metrics(graph)
