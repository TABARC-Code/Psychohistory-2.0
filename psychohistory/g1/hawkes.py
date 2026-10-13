import numpy as np
from scipy.optimize import minimize


def fit_exponential_hawkes(events, T):
    """Fit a stationary exponential Hawkes model on the observation window [0, T]."""
    try:
        e = np.asarray(events, dtype=float)
        T = float(T)
    except (TypeError, ValueError):
        return {"status": "UNRESOLVED", "reason": "invalid numeric input"}
    if e.ndim != 1 or not np.isfinite(T) or T <= 0 or not np.all(np.isfinite(e)):
        return {"status": "UNRESOLVED", "reason": "invalid event array or observation window"}
    if np.any(e < 0) or np.any(e > T):
        return {"status": "UNRESOLVED", "reason": "events outside observation window"}
    if len(e) < 5:
        return {"status": "UNRESOLVED", "reason": "need >=5 events"}
    e = np.sort(e)
    # A continuous-time point process cannot order simultaneous rounded events.
    # Treat ties as unresolved instead of creating artificial self-excitation.
    if np.any(np.diff(e) == 0):
        return {"status": "UNRESOLVED",
                "reason": "tied timestamps: event ordering is unidentifiable"}

    def nll(z):
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            mu, alpha, beta = np.exp(z)
            n = alpha / beta
            if not np.isfinite(n) or n >= 0.999 or n < 0:
                return np.inf
            intensity = np.array([
                mu + alpha * np.exp(-beta * (ti - e[:i])).sum()
                for i, ti in enumerate(e)
            ])
            ll = np.log(intensity).sum() - mu * T - n * np.sum(-np.expm1(-beta * (T - e)))
            return float(-ll) if np.isfinite(ll) else np.inf

    initial = np.log([len(e) / T * 0.5, 0.2 / T, 1.0 / T])
    result = minimize(nll, initial, method="Nelder-Mead")
    if not result.success or not np.isfinite(result.fun):
        return {"status": "UNRESOLVED", "reason": "optimizer did not find a finite solution"}
    mu, alpha, beta = np.exp(result.x)
    n = alpha / beta
    if not np.all(np.isfinite([mu, alpha, beta, n])) or n >= 0.999:
        return {"status": "UNRESOLVED", "reason": "invalid or unstable fit"}
    return {"status": "VALID", "mu": float(mu), "alpha": float(alpha),
            "beta": float(beta), "branching_ratio": float(n),
            "log_likelihood": float(-result.fun)}
