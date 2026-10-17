"""G23 numerical screening; predictive admission requires independent verification.

The caller-supplied flags are hypotheses about evidence quality, not proof of
registered holdouts, provenance, measurement validity or multiplicity control.
No public admission API exists until those checks are implemented and tested.
"""
from math import isfinite


def coupling_gate(*, out_of_sample_gain=None, valid_null=False,
                  identifiable=False, multiplicity_corrected=False):
    reasons = []
    if (isinstance(out_of_sample_gain, bool)
            or not isinstance(out_of_sample_gain, (int, float))
            or not _finite_positive(out_of_sample_gain)):
        reasons.append("no finite positive held-out gain")
    for flag, message in (
        (valid_null, "null unresolved"),
        (identifiable, "weak identifiability"),
        (multiplicity_corrected, "multiplicity unresolved"),
    ):
        if type(flag) is not bool or not flag:
            reasons.append(message)

    candidate_numerically_eligible = not reasons
    # This function cannot inspect observation ancestry, first-available
    # timestamps, immutable registrations, outcome contracts, or holdout data.
    # A caller can set every flag to True; that must never authorise admission.
    reasons.append("independent provenance and holdout verification unavailable")
    return {
        "status": "TEST_UNRESOLVED",
        "reasons": reasons,
        "candidate_numerically_eligible": candidate_numerically_eligible,
        "provenance_status": "UNVERIFIED",
        "predictive_input": False,
    }


def _finite_positive(value):
    try:
        return isfinite(value) and value > 0
    except (TypeError, ValueError, OverflowError):
        return False
