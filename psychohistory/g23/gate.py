import math
from numbers import Real


def coupling_gate(
    *,
    out_of_sample_gain=None,
    valid_null=False,
    identifiable=False,
    multiplicity_corrected=False,
):
    reasons = []
    gain = out_of_sample_gain
    if (
        isinstance(gain, bool)
        or not isinstance(gain, Real)
        or not math.isfinite(gain)
        or gain <= 0
    ):
        reasons.append("no finite positive held-out gain")
    if valid_null is not True:
        reasons.append("null unresolved")
    if identifiable is not True:
        reasons.append("weak identifiability")
    if multiplicity_corrected is not True:
        reasons.append("multiplicity unresolved")
    return {"status": "ADMITTED" if not reasons else "TEST_UNRESOLVED", "reasons": reasons}
