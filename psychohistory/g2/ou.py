import numpy as np
from scipy.optimize import minimize


def fit_ou(times, values):
    """Fit an OU transition model, refusing invalid or unidentifiable inputs."""
    try:
        t = np.asarray(times, dtype=float)
        x = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError):
        return {"status": "UNRESOLVED", "reason": "invalid numeric input"}
    if t.ndim != 1 or x.ndim != 1 or len(t) != len(x):
        return {"status": "UNRESOLVED", "reason": "time/value dimension mismatch"}
    if len(x) < 4:
        return {"status": "UNRESOLVED", "reason": "need >=4 observations"}
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(x)):
        return {"status": "UNRESOLVED", "reason": "nonfinite observations"}
    with np.errstate(over="ignore", invalid="ignore"):
        dt = np.diff(t)
    if not np.all(np.isfinite(dt)) or np.any(dt <= 0):
        return {"status": "UNRESOLVED", "reason": "timestamps must be strictly increasing"}
    # Absolute series levels must not change OU identifiability: the OU
    # likelihood is translation-equivariant. Reject only spreads that are
    # indistinguishable from floating-point rounding at the observed level.
    with np.errstate(over="ignore", invalid="ignore"):
        spread = float(np.ptp(x))
        precision = float(np.spacing(np.max(np.abs(x))))
        centred = (x - x[0]) / spread if spread > 0 else x - x[0]
    if (not np.isfinite(spread) or not np.all(np.isfinite(centred))
            or spread <= 32 * precision):
        return {"status": "UNRESOLVED", "reason": "near-constant or unrepresentable series"}
    # Fit in dimensionless time to avoid unit-dependent optimiser bounds.
    # For u=(t-t0)/span, a_u=a_t*span and sigma_u=sigma_t*sqrt(span).
    with np.errstate(over="ignore", invalid="ignore"):
        span = float(t[-1] - t[0])
    if not np.isfinite(span) or span <= 0:
        return {"status": "UNRESOLVED", "reason": "invalid time span"}
    dt = dt / span
    if not np.all(np.isfinite(dt)) or np.any(dt <= 0):
        return {"status": "UNRESOLVED", "reason": "unresolvable time spacing"}
    prev, nxt = centred[:-1], centred[1:]

    def nll(z):
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            a = np.exp(z[0])
            mu = z[1]
            sigma = np.exp(z[2])
            decay = np.exp(-a * dt)
            mean = mu + (prev - mu) * decay
            variance = sigma**2 * (-np.expm1(-2 * a * dt)) / (2 * a)
            if not np.all(np.isfinite(variance)) or np.any(variance <= 0):
                return np.inf
            value = 0.5 * np.sum(np.log(2 * np.pi * variance) + (nxt - mean)**2 / variance)
            return float(value) if np.isfinite(value) else np.inf

    # The likelihood can have shallow local optima. Compare finite converged
    # fits from a small fixed multi-start grid rather than trusting one start.
    mu_start = float(np.mean(centred))
    sigma_start = np.log(max(float(np.std(centred)), 1e-6))
    candidates = [
        minimize(nll, [np.log(rate), mu_start, sigma_start],
                 method="L-BFGS-B", bounds=[(-15, 15), (None, None), (-20, 20)])
        for rate in (0.1, 1.0, 10.0, 100.0)
    ]
    finite = [r for r in candidates if r.success and np.isfinite(r.fun)]
    if not finite:
        return {"status": "UNRESOLVED", "reason": "optimizer did not find a finite solution"}
    result = min(finite, key=lambda r: r.fun)
    if not result.success or not np.isfinite(result.fun):
        return {"status": "UNRESOLVED", "reason": "optimizer did not find a finite solution"}
    a_u, mu_centred, sigma_u = np.exp(result.x[0]), result.x[1], np.exp(result.x[2])
    # Undo value and time normalisation; correct conditional-density Jacobian.
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        mu = mu_centred * spread + x[0]
        a = a_u / span
        sigma = sigma_u * spread / np.sqrt(span)
        log_likelihood = -result.fun - (len(x) - 1) * np.log(spread)
    if not np.all(np.isfinite([a, mu, sigma, log_likelihood])) or a <= 0 or sigma <= 0:
        return {"status": "UNRESOLVED", "reason": "invalid physical parameter scaling"}
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        recovery_time = float(np.divide(1.0, a))
    if not np.isfinite(recovery_time) or recovery_time <= 0:
        return {"status": "UNRESOLVED", "reason": "nonfinite recovery time"}
    return {"status": "VALID", "a": float(a), "mu": float(mu),
            "sigma": float(sigma), "recovery_time": recovery_time,
            "log_likelihood": float(log_likelihood),
            "boundary_warning": bool(a_u < 1e-4 or np.isclose(result.x[0], -15) or np.isclose(result.x[0], 15))}
