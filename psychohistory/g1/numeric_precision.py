"""Strict finite binary64 input boundary for Hawkes event measurements.

A longdouble observation cannot be rounded before event-window membership,
ordering and likelihood are computed. This guard deliberately rejects values
not representable in the estimator's float64 working precision.
"""

from numbers import Integral, Real

import numpy as np


def exact_binary64_real(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        return False
    try:
        if isinstance(value, Integral) and abs(int(value)) > 2**53:
            return False
        converted = float(value)
        return bool(np.isfinite(converted) and value == converted)
    except (TypeError, ValueError, OverflowError):
        return False
