"""Observed-prehistory exponential Hawkes diagnostic (separate from legacy fit).

This conditions the finite-window likelihood on events measured strictly before
window start. It cannot establish endogenous transmission, identifiability or
predictive admission. Caller must validate provenance and availability times.
"""

import numpy as np
from scipy.optimize import minimize

from .numeric_precision import exact_binary64_real


def _real_vector(values):
    """Refuse complex values before any potentially lossy float conversion."""
    raw = np.asarray(values, dtype=object)
    if raw.ndim != 1:
        raise ValueError("expected one-dimensional real event times")
    if any(not exact_binary64_real(v) for v in raw):
        raise ValueError("invalid event time type or precision loss")
    result = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(result)):
        raise ValueError("nonfinite event times")
    return result


def _prepared(events, prehistory, T):
    if not exact_binary64_real(T):
        raise ValueError("invalid window type or precision loss")
    T = float(T)
    if not np.isfinite(T) or T <= 0:
        raise ValueError("invalid window")
    events = _real_vector(events)
    past = _real_vector(prehistory)
    if (np.any(events < 0) or np.any(events >= T)
            or np.any(past >= 0)):
        raise ValueError("events outside their respective windows")
    events = np.sort(events)
    past = np.sort(past)
    if (np.any(np.diff(events) <= 0) or np.any(np.diff(past) <= 0)):
        raise ValueError("tied timestamps")
    u = events / T
    p = past / T
    # Both sides of the window origin matter: a positive in-window event
    # cannot be silently rounded onto zero, nor can a negative prehistory
    # event become an event exactly at the origin during normalisation.
    if (not np.all(np.isfinite(u)) or not np.all(np.isfinite(p))
            or np.any((events > 0) & (u == 0))
            or np.any((past < 0) & (p == 0))
            or np.any(np.diff(u) <= 0) or np.any(np.diff(p) <= 0)
            or np.any(u >= 1)):
        raise ValueError("event precision collapse")
    return u, p, T


def _log_likelihood_unit_window_observed_history(u, p, mu, alpha, beta):
    """Exact conditional log likelihood on [0,1), with p<0 observed.

    History at the window start is H0=sum(exp(beta*p_j)). The compensator
    integrates both this decaying initial intensity and in-window events.
    """
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        if (not np.all(np.isfinite([mu, alpha, beta])) or mu < 0
                or alpha < 0 or beta <= 0):
            return -np.inf
        h0 = float(np.sum(np.exp(beta * p)))
        history = h0
        previous = 0.0
        log_intensity = 0.0
        for t in u:
            history *= np.exp(-beta * (t - previous))
            intensity = mu + alpha * history
            if not np.isfinite(intensity) or intensity <= 0:
                return -np.inf
            log_intensity += np.log(intensity)
            history += 1.0
            previous = t
        compensator = mu + (alpha / beta) * (
            h0 * (-np.expm1(-beta))
            + np.sum(-np.expm1(-beta * (1.0 - u)))
        )
        score = log_intensity - compensator
        return float(score) if np.isfinite(score) else -np.inf


def conditional_hawkes_log_likelihood(events, T, *, prehistory=(), mu, alpha, beta):
    """Score a fixed physical-parameter model, conditional on observed history.

    This is an explanatory likelihood, not a registered forecast. Prehistory
    and event timestamps must be independently verified by the caller.
    """
    u, p, T = _prepared(events, prehistory, T)
    if any(not exact_binary64_real(v) for v in (mu, alpha, beta)):
        raise ValueError("model parameter precision loss or invalid numeric type")
    mu_u, alpha_u, beta_u = float(mu) * T, float(alpha) * T, float(beta) * T
    ll = _log_likelihood_unit_window_observed_history(u, p, mu_u, alpha_u, beta_u)
    return float(ll - len(u) * np.log(T)) if np.isfinite(ll) else -np.inf


def fit_exponential_hawkes_observed_prehistory(events, T, *, prehistory=()):
    """Separate non-admitted diagnostic with observed pre-window events.

    Uses dimensionless time and the legacy multi-start search strategy.
    Identifiability is still unverified even if numerical optimisation succeeds.
    """
    try:
        u, p, T = _prepared(events, prehistory, T)
    except (TypeError, ValueError, OverflowError) as exc:
        return {"status": "UNRESOLVED", "reason": str(exc), "predictive_input": False}
    if len(u) < 5:
        return {"status": "UNRESOLVED", "reason": "need >=5 events", "predictive_input": False}

    def nll(z):
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            mu, alpha, beta = np.exp(z)
            branching = alpha / beta
            if not np.isfinite(branching) or branching < 0 or branching >= 0.999:
                return np.inf
            ll = _log_likelihood_unit_window_observed_history(u, p, mu, alpha, beta)
            return float(-ll) if np.isfinite(ll) else np.inf

    rate = float(len(u))
    starts = (
        (0.5 * rate, 0.2, 1.0), (0.9 * rate, 0.5, 5.0),
        (0.3 * rate, 5.0, 10.0), (0.7 * rate, 10.0, 20.0),
        (0.5 * rate, 0.05, 0.1), (0.5 * rate, 50.0, 100.0),
    )
    candidates = [minimize(nll, np.log(start), method="Nelder-Mead")
                  for start in starts]
    finite = [r for r in candidates if r.success and np.isfinite(r.fun)]
    if not finite:
        return {"status": "UNRESOLVED", "reason": "optimiser did not converge",
                "predictive_input": False}
    best = min(finite, key=lambda r: r.fun)
    mu_u, alpha_u, beta_u = np.exp(best.x)
    branching = alpha_u / beta_u
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        mu, alpha, beta = np.array([mu_u, alpha_u, beta_u]) / T
    if not np.all(np.isfinite([mu, alpha, beta, branching])):
        return {"status": "UNRESOLVED", "reason": "invalid physical scaling",
                "predictive_input": False}
    # Conditional prehistory does not rescue alpha≈beta≈0 degeneracy:
    # the model then matches a homogeneous Poisson null while alpha/beta
    # can take an arbitrary value. Use the same dimensionless guard as the
    # zero-prehistory estimator; it is not a predictive skill test.
    poisson_ll_u = len(u) * (np.log(len(u)) - 1.0)
    null_gain_u = float(-best.fun - poisson_ll_u)
    null_tol = 1e-8 * max(1.0, abs(poisson_ll_u))
    if beta_u <= 1e-3 or null_gain_u <= null_tol:
        return {"status": "UNRESOLVED",
                "reason": "decay or excitation unidentifiable against in-sample Poisson null",
                "branching_ratio_candidate": float(branching), "predictive_input": False}
    if branching <= 1e-4 or branching >= 0.9989:
        return {"status": "UNRESOLVED", "reason": "excitation boundary unidentifiable",
                "branching_ratio_candidate": float(branching), "predictive_input": False}
    return {"status": "VALID", "mu": float(mu), "alpha": float(alpha),
            "beta": float(beta), "branching_ratio": float(branching),
            "log_likelihood": float(-best.fun - len(u) * np.log(T)),
            "prehistory_event_count": int(len(p)),
            "prehistory_status": "OBSERVED_CONDITIONING_NOT_INDEPENDENTLY_VERIFIED",
            "identifiability_status": "UNVERIFIED", "predictive_input": False}
