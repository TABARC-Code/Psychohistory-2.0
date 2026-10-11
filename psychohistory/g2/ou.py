import numpy as np
from scipy.optimize import minimize


def fit_ou(times, values):
    """Fit an OU transition model, refusing invalid or unidentifiable inputs."""
    try:
        t = np.asarray(times, dtype=float)
        x = np.asarray(values, dtype=float)
    except (TypeError, ValueError):
        return {"status": "UNRESOLVED", "reason": "invalid numeric input"}
    if t.ndim != 1 or x.ndim != 1 or len(t) != len(x):
        return {"status": "UNRESOLVED", "reason": "time/value dimension mismatch"}
    if len(x) < 4:
        return {"status": "UNRESOLVED", "reason": "need >=4 observations"}
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(x)):
        return {"status": "UNRESOLVED", "reason": "nonfinite observations"}
    dt = np.diff(t)
    if np.any(dt <= 0):
        return {"status": "UNRESOLVED", "reason": "timestamps must be strictly increasing"}
    if np.ptp(x) <= 1e-10 * max(1.0, float(np.max(np.abs(x)))):
        return {"status": "UNRESOLVED", "reason": "near-constant series: parameters unidentifiable"}
    prev, nxt = x[:-1], x[1:]

    def nll(z):
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            a = np.exp(z[0]); mu = z[1]; sigma = np.exp(z[2])
            decay = np.exp(-a * dt)
            mean = mu + (prev - mu) * decay
            variance = sigma**2 * (-np.expm1(-2 * a * dt)) / (2 * a)
            if not np.all(np.isfinite(variance)) or np.any(variance <= 0):
                return np.inf
            value = 0.5 * np.sum(np.log(2 * np.pi * variance) + (nxt - mean)**2 / variance)
            return float(value) if np.isfinite(value) else np.inf

    initial = [np.log(0.1), float(np.mean(x)), np.log(max(float(np.std(x)), 1e-6))]
    result = minimize(nll, initial, method="L-BFGS-B",
                      bounds=[(-15, 15), (None, None), (-20, 20)])
    if not result.success or not np.isfinite(result.fun):
        return {"status": "UNRESOLVED", "reason": "optimizer did not find a finite solution"}
    a, mu, sigma = np.exp(result.x[0]), result.x[1], np.exp(result.x[2])
    return {"status": "VALID", "a": float(a), "mu": float(mu),
            "sigma": float(sigma), "recovery_time": float(1 / a),
            "log_likelihood": float(-result.fun),
            "boundary_warning": bool(a < 1e-4 or np.isclose(result.x[0], -15) or np.isclose(result.x[0], 15))}
