"""Strict finite binary64 input boundary for numerical measurement estimators.

Check original scalar types before NumPy promotes or rounds a mixed array.
The working estimators use float64; values that would change on conversion
must not be treated as the original measurements.
"""

from numbers import Integral, Real

import numpy as np


def exact_binary64_real(value):
    """Accept finite real scalars exactly representable as binary64.

    Conservatively refuse integer magnitudes beyond 2**53 even when a
    particular larger integer happens to be exactly representable.
    """
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        return False
    try:
        if isinstance(value, Integral) and abs(int(value)) > 2**53:
            return False
        converted = float(value)
        return bool(np.isfinite(converted) and value == converted)
    except (TypeError, ValueError, OverflowError):
        return False
