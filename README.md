# Psychohistory 2.4 — executable research engine

This repository implements the Psychohistory 2.4 specification as an auditable point-in-time analysis system. It is a research framework, not a claim that historical or social systems are deterministically predictable.

## Non-negotiable rules

1. **Measurement Validity:** an unquantified, unidentified or unvalidated quantity is not yet a measurement.
2. **Evidence Independence:** distinct labels do not imply independent evidence.
3. **Network Inference:** a locally valid/significant result is not automatically a globally valid discovery.
4. Every evaluation is point-in-time. `available_at > as_of` is future information and is rejected.
5. Unknown validation statistics remain `UNMEASURED`; the engine never fabricates Brier scores, calibration, false-alert rates or lead time.
6. Experimental modules do not become predictive inputs merely by producing a statistic.

## Install and run

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
psychohistory evaluate --as-of 2026-10-06T17:00:00+00:00
```

## Implemented in v0.1

The runnable spine includes SQLite vintage storage, point-in-time reconstruction, observation ancestry, revision and transaction-pipeline metadata, immutable forecast IDs, matured-outcome scoring, base-rate/persistence baselines, exact-transition OU estimation, exponential Hawkes estimation, Laplacian fragmentation metrics, Brier/Brier-skill scoring and a conservative G23 admission gate.

G23, anchors and domain sidecars remain **experimental**. Their presence in the repository is not empirical validation.

## Canonical specification

The complete mathematical specification is maintained as a versioned project artifact. Binary canonical documents are intentionally not injected through the GitHub text-content connector; implementation changes must state which specification contract they implement and must not silently upgrade candidate models to validated evidence.

## GitHub Actions

`CI` runs tests on Python 3.11/3.12. `Scheduled evaluation` can run daily or manually and uploads the JSON evaluation as an artifact. It does not download arbitrary live data: source adapters must preserve publication time, vintage and provenance before they are admitted.
