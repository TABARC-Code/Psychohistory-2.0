"""G23 held-out coupling diagnostic. Not an empirical admission authority.

Four caller-supplied flags can screen an estimate, but cannot establish
registration, measurement validity, source independence, or Outcome Contracts.
The current engine has no trusted verifier for those conditions, so it must
never return ADMITTED or mark a predictor as eligible for operational use.
"""

import math
from numbers import Real


def coupling_gate(
    *,
    out_of_sample_gain=None,
    valid_null=False,
    identifiable=False,
    multiplicity_corrected=False,
):
    """Fail closed on non-finite gains and unverified predictive admission."""
    reasons = []
    gain = out_of_sample_gain
    try:
        finite_positive = (
            not isinstance(gain, bool)
            and isinstance(gain, Real)
            and math.isfinite(gain)
            and gain > 0
        )
    except (TypeError, ValueError, OverflowError):
        finite_positive = False
    if not finite_positive:
        reasons.append("no finite positive held-out gain")
    if valid_null is not True:
        reasons.append("null unresolved")
    if identifiable is not True:
        reasons.append("weak identifiability")
    if multiplicity_corrected is not True:
        reasons.append("multiplicity unresolved")
    diagnostic_passed = not reasons
    if diagnostic_passed:
        reasons.append("independent registration, measurement, ancestry and outcome-contract evidence unverified")
    return {
        "status": "CANDIDATE_NOT_ADMITTED" if diagnostic_passed else "TEST_UNRESOLVED",
        "diagnostic_passed": diagnostic_passed,
        "predictive_input": False,
        "evidence_independence": "UNVERIFIED",
        "measurement_validity": "REQUIRES_EXTERNAL_PROVENANCE",
        "registration_provenance": "UNVERIFIED",
        "network_inference": "NOT_ESTABLISHED",
        "reasons": reasons,
    }
