import sqlite3
from datetime import UTC, datetime, timedelta

from psychohistory.core.models import Forecast, Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.g2.ou import fit_ou
from psychohistory.g3.spectral import laplacian_metrics
from psychohistory.g23.gate import coupling_gate
from psychohistory.validation.scoring import brier


def T(days):
    return datetime(2020, 1, 1, tzinfo=UTC) + timedelta(days=days)


def test_asof_blocks_future(tmp_path):
    store = Store(tmp_path / "x.db")
    store.add_observation(Observation("a", "x", T(0), T(2), 1, "src"))
    assert not store.observations_as_of(T(1))
    assert len(store.observations_as_of(T(2))) == 1


def test_forecasts_immutable(tmp_path):
    store = Store(tmp_path / "x.db")
    forecast = Forecast("f", "e", T(0), T(1), 0.2, "m", 0.3)
    store.add_forecast(forecast)
    try:
        store.add_forecast(forecast)
        assert False
    except sqlite3.IntegrityError:
        pass


def test_score_only_matured(tmp_path):
    store = Store(tmp_path / "x.db")
    store.add_forecast(Forecast("f", "e", T(0), T(2), 0.2, "m", 0.3))
    store.resolve("e", 1, T(1))
    assert store.scored() == []


def test_brier():
    rows = [("f", 0.2, 0.4, 0), ("g", 0.8, 0.6, 1)]
    result = brier(rows)
    assert abs(result["brier"] - 0.04) < 1e-9
    assert result["brier_skill"] > 0


def test_ancestry_breadth():
    observations = [
        Observation("a", "x", T(0), T(0), 1, "s", ancestry=("shock",)),
        Observation("b", "y", T(0), T(0), 2, "s", ancestry=("shock",)),
    ]
    result = validate_observations(observations, T(1))
    assert result["informational_breadth_upper_bound"] == 1


def test_ou_and_graph():
    result = fit_ou(range(8), [1, 0.8, 0.7, 0.55, 0.5, 0.42, 0.4, 0.35])
    assert result["status"] in {"VALID", "UNRESOLVED"}
    graph = laplacian_metrics([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert graph["lambda2"] > 0


def test_g23_refuses_weak_evidence():
    assert coupling_gate(out_of_sample_gain=0.1)["status"] == "TEST_UNRESOLVED"


def test_memetic_copy_is_propagation_not_independent_origin():
    observations = [
        Observation(
            "m1", "g1:meme", T(0), T(0), 1, "social",
            evidence_role="propagation", content_ancestry=("meme-root",),
            carrier="social", actor_id="a", community_id="c1",
            semantic_variant="v1",
        ),
        Observation(
            "m2", "g1:meme", T(1), T(1), 1, "social",
            evidence_role="propagation", content_ancestry=("meme-root",),
            carrier="social", actor_id="b", community_id="c2",
            semantic_variant="v1",
        ),
        Observation(
            "m3", "g1:meme", T(2), T(2), 1, "news",
            evidence_role="propagation", content_ancestry=("meme-root",),
            carrier="news", actor_id="c", community_id="c3",
            semantic_variant="v2",
        ),
    ]
    result = validate_observations(observations, T(3))
    assert result["content_origin_breadth_upper_bound"] == 1
    assert result["propagation_event_count"] == 3
    assert result["carrier_breadth"] == 2
    assert result["community_breadth"] == 3
    assert result["semantic_variant_breadth"] == 2


def test_memetic_resonance_does_not_assert_endorsement_or_attribution():
    from psychohistory.g1.memetics import analyse_memetic_observations

    observations = [
        Observation(
            f"m{i}", "g1:meme", T(i), T(i), 1, "social",
            evidence_role="propagation", content_ancestry=("root",),
            carrier="social", actor_id=f"a{i}", community_id=f"c{i % 2}",
            semantic_variant=f"v{i % 2}",
        )
        for i in range(5)
    ]
    result = analyse_memetic_observations(observations)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["propagation"]["events"] == 5
    assert result["social_resonance"]["endogenous_reproduction_fraction"] > 0
    assert result["coordination"]["status"] == "UNRESOLVED"
    assert result["attribution"]["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
