"""Arithmetic-only Brier diagnostics; not a forecast-admission authority.

Registration, maturity, outcome vintage, observation ancestry and independent
holdouts must be verified before supplying rows. No result here can authorise
G23 predictive use.
"""
from math import isfinite
from numbers import Real

from ..core.validation import _valid_primary_label


def _probability(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        return False
    try:
        return bool(isfinite(value) and 0 <= value <= 1)
    except (TypeError, ValueError, OverflowError):
        return False


def brier(rows):
    """Score (forecast_id, probability, baseline_probability, binary_outcome).

    Reject malformed rows rather than reporting an invalid score as measured.
    A missing baseline permits a Brier score but not a skill comparison.
    """
    try:
        rows = list(rows)
    except (TypeError, ValueError):
        return {"status": "UNRESOLVED", "reason": "invalid scoring rows", "n": 0}
    if not rows:
        return {"status": "UNMEASURED", "n": 0}

    ids = set()
    for index, row in enumerate(rows):
        if not isinstance(row, (tuple, list)) or len(row) != 4:
            return {"status": "UNRESOLVED", "n": 0,
                    "reason": f"invalid scoring row shape at index {index}"}
        forecast_id, probability, baseline, outcome = row
        if not _valid_primary_label(forecast_id):
            return {"status": "UNRESOLVED", "n": 0,
                    "reason": f"invalid forecast identifier at index {index}"}
        if forecast_id in ids:
            return {"status": "UNRESOLVED", "n": 0,
                    "reason": "duplicate forecast identifier"}
        ids.add(forecast_id)
        if (not _probability(probability) or
                (baseline is not None and not _probability(baseline)) or
                type(outcome) is not int or outcome not in (0, 1)):
            return {"status": "UNRESOLVED", "n": 0,
                    "reason": f"invalid probability, baseline or binary outcome at index {index}"}

    bs = sum((row[1] - row[3]) ** 2 for row in rows) / len(rows)
    out = {"status": "MEASURED", "n": len(rows), "brier": bs,
           "validation_scope": "ARITHMETIC_ONLY", "predictive_input": False}
    if all(row[2] is not None for row in rows):
        bb = sum((row[2] - row[3]) ** 2 for row in rows) / len(rows)
        skill = None
        if bb > 0:
            ratio = bs / bb
            if isfinite(ratio):
                skill = 1 - ratio
        out.update(baseline_brier=bb, brier_skill=skill)
    return out
