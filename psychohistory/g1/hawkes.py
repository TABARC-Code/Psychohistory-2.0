"""Exponential Hawkes diagnostic with dimensionless fitting.

Numerical convergence is not evidence of identifiable excitation or causal
transmission. This model assumes no observed pre-window history.
"""

import numpy as np
from scipy.optimize import minimize


def _log_likelihood_unit_window(u, mu, alpha, beta):
    """Exact finite-window exponential Hawkes log likelihood, O(n) in events.

    Events must be strictly ordered in [0, 1]. With no pre-window history,
    S_i = exp(-beta * (u_i - u_{i-1})) * (1 + S_{i-1}), S_0 = 0.
    The compensator includes the right-censoring term for every event.
    """
    previous = None
    history = 0.0
    log_intensity = 0.0
    for time in u:
        if previous is not None:
            history = np.exp(-beta * (time - previous)) * (1.0 + history)
        intensity = mu + alpha * history
        if not np.isfinite(intensity) or intensity <= 0:
            return -np.inf
        log_intensity += np.log(intensity)
        previous = time
    compensator = mu + (alpha / beta) * np.sum(-np.expm1(-beta * (1.0 - u)))
    return float(log_intensity - compensator)


def fit_exponential_hawkes(events, T):
    """Fit a zero-prehistory exponential Hawkes diagnostic on [0, T]."""
    try:
        e = np.asarray(events, dtype=float)
        T = float(T)
    except (TypeError, ValueError, OverflowError):
        return {"status": "UNRESOLVED", "reason": "invalid numeric input"}
    if e.ndim != 1 or not np.isfinite(T) or T <= 0 or not np.all(np.isfinite(e)):
        return {"status": "UNRESOLVED", "reason": "invalid event array or observation window"}
    if np.any(e < 0) or np.any(e > T):
        return {"status": "UNRESOLVED", "reason": "events outside observation window"}
    if len(e) < 5:
        return {"status": "UNRESOLVED", "reason": "need >=5 events"}
    e = np.sort(e)
    if np.any(np.diff(e) == 0):
        return {"status": "UNRESOLVED",
                "reason": "tied timestamps: event ordering is unidentifiable"}

    # Dimensionless time u=t/T. Fitting on [0,1] prevents arbitrary physical
    # time units from changing the optimiser's search geometry. Rates are
    # transformed back to their physical units after optimisation.
    u = e / T
    # A strictly positive event must not underflow onto the window origin.
    # Otherwise the fit silently changes the observed event chronology.
    if np.any((e > 0) & (u == 0)):
        return {"status": "UNRESOLVED",
                "reason": "event times collapse to window origin at normalised precision",
                "predictive_input": False}
    if np.any(np.diff(u) <= 0):
        return {"status": "UNRESOLVED",
                "reason": "event times collapse at observation-window precision"}

    def nll(z):
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            mu, alpha, beta = np.exp(z)
            branching = alpha / beta
            if not np.isfinite(branching) or branching >= 0.999 or branching < 0:
                return np.inf
            ll = _log_likelihood_unit_window(u, mu, alpha, beta)
            return float(-ll) if np.isfinite(ll) else np.inf

    # Multi-start reduces, but cannot eliminate, local-optimum sensitivity.
    rate = float(len(e))
    starts = (
        (0.5 * rate, 0.2, 1.0),
        (0.9 * rate, 0.5, 5.0),
        (0.3 * rate, 5.0, 10.0),
        (0.7 * rate, 10.0, 20.0),
        (0.5 * rate, 0.05, 0.1),
        (0.5 * rate, 50.0, 100.0),
    )
    candidates = [minimize(nll, np.log(start), method="Nelder-Mead")
                  for start in starts]
    finite = [r for r in candidates if r.success and np.isfinite(r.fun)]
    if not finite:
        return {"status": "UNRESOLVED", "reason": "optimizer did not find a finite solution"}
    result = min(finite, key=lambda r: r.fun)
    if not result.success or not np.isfinite(result.fun):
        return {"status": "UNRESOLVED", "reason": "optimizer did not find a finite solution"}
    mu_u, alpha_u, beta_u = np.exp(result.x)
    branching = alpha_u / beta_u
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        mu, alpha, beta = np.array([mu_u, alpha_u, beta_u]) / T
    if (not np.all(np.isfinite([mu, alpha, beta, branching]))
            or branching >= 0.999):
        return {"status": "UNRESOLVED", "reason": "invalid or unstable fit"}
    if branching <= 1e-4:
        return {"status": "UNRESOLVED",
                "reason": "near-zero excitation: decay rate unidentifiable",
                "branching_ratio_candidate": float(branching),
                "predictive_input": False}
    if branching >= 0.9989:
        return {"status": "UNRESOLVED",
                "reason": "branching ratio at stability boundary",
                "branching_ratio_candidate": float(branching),
                "predictive_input": False}
    return {"status": "VALID", "mu": float(mu), "alpha": float(alpha),
            "beta": float(beta), "branching_ratio": float(branching),
            "log_likelihood": float(-result.fun - len(e) * np.log(T)),
            "identifiability_status": "UNVERIFIED", "predictive_input": False}
