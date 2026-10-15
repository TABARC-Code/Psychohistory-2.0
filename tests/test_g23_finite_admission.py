from math import inf, nan
from psychohistory.g23.gate import coupling_gate


def test_rejects_nonfinite_gain():
    for gain in (nan, inf, -inf, True, None, 0, -1):
        result = coupling_gate(out_of_sample_gain=gain, valid_null=True,
                               identifiable=True, multiplicity_corrected=True)
        assert result["status"] == "TEST_UNRESOLVED"
        assert result["predictive_input"] is False


def test_rejects_truthy_nonboolean_flags():
    for name in ("valid_null", "identifiable", "multiplicity_corrected"):
        flags = {"valid_null": True, "identifiable": True,
                 "multiplicity_corrected": True}
        flags[name] = "true"
        result = coupling_gate(out_of_sample_gain=0.1, **flags)
        assert result["status"] == "TEST_UNRESOLVED"


def test_valid_finite_gain_is_only_numerical_screening():
    result = coupling_gate(out_of_sample_gain=0.1, valid_null=True,
                           identifiable=True, multiplicity_corrected=True)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["diagnostic_passed"] is True
    assert result["predictive_input"] is False
    assert result["registration_provenance"] == "UNVERIFIED"
    assert result["network_inference"] == "NOT_ESTABLISHED"


def test_no_caller_assertions_can_grant_predictive_admission():
    for gain in (0.001, 1.0, 1000.0):
        result = coupling_gate(out_of_sample_gain=gain, valid_null=True,
                               identifiable=True, multiplicity_corrected=True)
        assert result["status"] != "ADMITTED"
        assert result["predictive_input"] is False
