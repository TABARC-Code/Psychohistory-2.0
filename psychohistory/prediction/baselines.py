"""Arithmetic baselines only; registration and chronology are verified elsewhere.

These functions cannot establish whether an outcome was available at a forecast
origin. They must not be used as independent proof of prospective skill.
"""
from math import isfinite
from numbers import Real


def _sequence(values):
    if isinstance(values, (str, bytes, bytearray, dict)):
        return None
    try:
        return tuple(values)
    except (TypeError, ValueError, OverflowError):
        return None


def _finite_real(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        return False
    try:
        return bool(isfinite(value))
    except (TypeError, ValueError, OverflowError):
        return False


def _arithmetic_result(**fields):
    return {
        "status": "VALID",
        "validation_scope": "ARITHMETIC_ONLY",
        "chronology_status": "UNVERIFIED",
        "predictive_input": False,
        **fields,
    }


def base_rate(outcomes):
    rows = _sequence(outcomes)
    if rows is None:
        return {"status": "UNRESOLVED", "reason": "invalid outcome sequence", "predictive_input": False}
    if not rows:
        return {"status": "UNMEASURED", "predictive_input": False}
    if any(type(value) is not int or value not in (0, 1) for value in rows):
        return {"status": "UNRESOLVED", "reason": "outcomes must be binary integers", "predictive_input": False}
    return _arithmetic_result(probability=sum(rows) / len(rows), n=len(rows))


def persistence(values):
    rows = _sequence(values)
    if rows is None:
        return {"status": "UNRESOLVED", "reason": "invalid value sequence", "predictive_input": False}
    if not rows:
        return {"status": "UNMEASURED", "predictive_input": False}
    if any(not _finite_real(value) for value in rows):
        return {"status": "UNRESOLVED", "reason": "values must be finite real numbers", "predictive_input": False}
    return _arithmetic_result(prediction=rows[-1])
