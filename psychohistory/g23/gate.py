"""G23 coupling admission: conservative numerical and evidence-flag checks.

These flags remain caller assertions; provenance and independent validation
must be checked upstream before interpreting ADMITTED as operational evidence.
"""
from math import isfinite


def coupling_gate(*, out_of_sample_gain=None, valid_null=False,
                  identifiable=False, multiplicity_corrected=False):
    reasons = []
    if (isinstance(out_of_sample_gain, bool)
            or not isinstance(out_of_sample_gain, (int, float))
            or not _finite_positive(out_of_sample_gain)):
        reasons.append("no finite positive held-out gain")
    for name, flag, message in (
        ("valid_null", valid_null, "null unresolved"),
        ("identifiable", identifiable, "weak identifiability"),
        ("multiplicity_corrected", multiplicity_corrected, "multiplicity unresolved"),
    ):
        if type(flag) is not bool or not flag:
            reasons.append(message)
    return {"status": "ADMITTED" if not reasons else "TEST_UNRESOLVED",
            "reasons": reasons}


def _finite_positive(value):
    try:
        return isfinite(value) and value > 0
    except (TypeError, ValueError, OverflowError):
        return False
