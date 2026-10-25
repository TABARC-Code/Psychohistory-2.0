"""Lag registry identity and claimed evidence are structural, not causal proof."""
import pytest

from psychohistory.core.bidirectional import DirectedHypothesis, reciprocal_view


@pytest.mark.parametrize("source,target", [
    (" ", "economy"), ("technology", "\t"),
    ("\n", " "), ("technology", "technology"),
    ("technology", " technology "),
])
def test_reject_empty_or_equivalent_domain_labels(source, target):
    with pytest.raises(ValueError):
        DirectedHypothesis(source, target, 1)


@pytest.mark.parametrize("evidence_ids", [
    "report-1", ["report-1"], {"report-1"}, 1,
    ("",), ("   ",), (42,), (None,),
    ("report-1", "report-1"),
])
def test_reject_malformed_or_duplicated_evidence_ids(evidence_ids):
    with pytest.raises(ValueError):
        DirectedHypothesis("industry", "narratives", 3, evidence_ids=evidence_ids)


def test_valid_distinct_evidence_ids_do_not_authorise_admission():
    forward = DirectedHypothesis("industry", "narratives", 3,
                                 coefficient=0.2, admitted=True,
                                 evidence_ids=("physical-1", "narrative-1"))
    reverse = DirectedHypothesis("narratives", "industry", 7,
                                 evidence_ids=("independent-2",))
    rows = reciprocal_view([forward, reverse])
    assert rows[0]["reverse_present"] is True
    assert rows[0]["admission_claimed_unverified"] is True
    assert all(row["admitted"] is False and row["predictive_input"] is False
               for row in rows)


def test_unknown_evidence_can_remain_explicitly_empty():
    row = DirectedHypothesis("health", "social", 14)
    assert row.evidence_ids == ()
    assert reciprocal_view([row])[0]["multiplicity_status"] == "UNVERIFIED"
