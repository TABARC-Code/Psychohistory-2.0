"""Arithmetic baselines only; registration and chronology are verified elsewhere.

These functions cannot establish whether an outcome was available at a forecast
origin. They must not be used as independent proof of prospective skill.
"""
from ..core.numeric_precision import exact_binary64_real


def _sequence(values):
    if isinstance(values, (str, bytes, bytearray, dict)):
        return None
    try:
        return tuple(values)
    except (TypeError, ValueError, OverflowError):
        return None


def _finite_real(value):
    # Persistence must not accept a value that the observation and scoring
    # boundaries would change when converted to binary64.
    return exact_binary64_real(value)


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
        return {"status": "UNRESOLVED", "reason": "values must be finite exact binary64 measurements", "predictive_input": False}
    return _arithmetic_result(prediction=float(rows[-1]))
