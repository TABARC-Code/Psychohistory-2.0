from datetime import UTC, datetime, timedelta

from psychohistory.core.bidirectional import DirectedHypothesis, reciprocal_view
from psychohistory.core.models import Forecast
from psychohistory.core.store import Store


def test_unverified_claim_does_not_become_bidirectional_admission():
    forward = DirectedHypothesis("energy", "narratives", 1,
                                 coefficient=0.4, admitted=True,
                                 evidence_ids=("unverified-claim",))
    backward = DirectedHypothesis("narratives", "energy", 3,
                                  coefficient=0.3, admitted=True,
                                  evidence_ids=("unverified-claim",))
    rows = reciprocal_view([forward, backward])
    assert all(not row["admitted"] for row in rows)
    assert all(not row["reverse_admitted"] for row in rows)
    assert all(row["admission_status"] == "UNVERIFIED" for row in rows)
    assert all(row["admission_claimed_unverified"] for row in rows)
    assert all(not row["predictive_input"] for row in rows)


def test_store_scoring_requires_verified_contract_and_registration(tmp_path):
    store = Store(tmp_path / "scoring.db")
    t = datetime(2026, 10, 17, tzinfo=UTC)
    store.add_forecast(Forecast("f", "unregistered", t,
                                t + timedelta(days=1), 0.8, "model", 0.5))
    store.resolve("unregistered", 1, t + timedelta(days=2), "first_release")
    store.resolve("unregistered", 0, t + timedelta(days=3), "revised")
    assert store.scored() == []
