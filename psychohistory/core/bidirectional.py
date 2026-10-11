"""Bidirectional hypothesis registry, without automatic causal admission.

A -> B and B -> A are separate hypotheses with their own evidence and lags.
This module does not estimate causal effects or feed predictions.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class DirectedHypothesis:
    source: str
    target: str
    lag_days: int
    coefficient: float | None = None
    admitted: bool = False
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.source or not self.target or self.source == self.target:
            raise ValueError("distinct nonempty source and target required")
        if self.lag_days < 0:
            raise ValueError("lag_days must be nonnegative")
        if self.coefficient is not None and not isfinite(self.coefficient):
            raise ValueError("coefficient must be finite")
        if self.admitted and (self.coefficient is None or not self.evidence_ids):
            raise ValueError("admission requires a finite coefficient and evidence")


def reciprocal_view(hypotheses):
    """Describe reciprocal hypotheses; never invent the missing reverse edge."""
    edges = {(h.source, h.target): h for h in hypotheses}
    if len(edges) != len(hypotheses):
        raise ValueError("duplicate directed hypothesis")
    return [
        {
            "source": h.source,
            "target": h.target,
            "lag_days": h.lag_days,
            "admitted": h.admitted,
            "reverse_present": (h.target, h.source) in edges,
            "reverse_admitted": edges[(h.target, h.source)].admitted
            if (h.target, h.source) in edges else False,
        }
        for h in hypotheses
    ]
