from math import inf, nan
from psychohistory.g23.gate import coupling_gate


def test_rejects_nonfinite_gain():
    for gain in (nan, inf, -inf, True, None, 0, -1):
        assert coupling_gate(out_of_sample_gain=gain, valid_null=True,
                             identifiable=True, multiplicity_corrected=True)["status"] != "ADMITTED"


def test_rejects_truthy_nonboolean_flags():
    for name in ("valid_null", "identifiable", "multiplicity_corrected"):
        flags = {"valid_null": True, "identifiable": True,
                 "multiplicity_corrected": True}
        flags[name] = "true"
        assert coupling_gate(out_of_sample_gain=0.1, **flags)["status"] != "ADMITTED"


def test_valid_finite_gain_with_boolean_evidence():
    assert coupling_gate(out_of_sample_gain=0.1, valid_null=True,
                         identifiable=True, multiplicity_corrected=True)["status"] == "ADMITTED"
