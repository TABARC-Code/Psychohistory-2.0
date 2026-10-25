"""Bidirectional lag-family registry; not a causal estimator.

Each direction and lag is a separate hypothesis. The registry does not
independently validate evidence provenance, multiplicity or predictive skill.
"""
from collections import Counter
from dataclasses import dataclass
from math import isfinite
from numbers import Real


@dataclass(frozen=True)
class DirectedHypothesis:
    source: str
    target: str
    lag_days: int
    coefficient: float | None = None
    admitted: bool = False
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self):
        # Whitespace-only or padded domain labels create artificial nodes
        # and can conceal a self-edge behind different spellings.
        if (type(self.source) is not str or not self.source.strip()
                or self.source != self.source.strip()
                or type(self.target) is not str or not self.target.strip()
                or self.target != self.target.strip()
                or self.source == self.target):
            raise ValueError("distinct canonical source and target required")
        if type(self.lag_days) is not int or self.lag_days < 0:
            raise ValueError("lag_days must be a nonnegative integer")
        if self.coefficient is not None:
            if (isinstance(self.coefficient, bool)
                    or not isinstance(self.coefficient, Real)):
                raise ValueError("coefficient must be finite")
            try:
                finite = isfinite(self.coefficient)
            except (ValueError, TypeError, OverflowError):
                finite = False
            if not finite:
                raise ValueError("coefficient must be finite")
        if type(self.admitted) is not bool:
            raise ValueError("admitted must be Boolean")
        # Evidence identifiers are provenance references, not arbitrary truthy
        # objects. Repeated or padded IDs must not imply independent support.
        if (type(self.evidence_ids) is not tuple
                or any(type(identifier) is not str or not identifier.strip()
                       or identifier != identifier.strip()
                       for identifier in self.evidence_ids)
                or len(set(self.evidence_ids)) != len(self.evidence_ids)):
            raise ValueError("evidence_ids must be distinct non-blank identifiers")
        if self.admitted and (self.coefficient is None or not self.evidence_ids):
            raise ValueError("admission requires a finite coefficient and evidence")


def reciprocal_view(hypotheses):
    """Show reciprocal lag families without inventing a reverse causal edge."""
    rows = list(hypotheses)
    edges = {(h.source, h.target, h.lag_days): h for h in rows}
    if len(edges) != len(rows):
        raise ValueError("duplicate directed hypothesis at the same lag")
    families = Counter((h.source, h.target) for h in rows)
    return [
        {
            "source": h.source,
            "target": h.target,
            "lag_days": h.lag_days,
            "admitted": False,
            "admission_claimed_unverified": h.admitted,
            "admission_status": "UNVERIFIED",
            "lag_family_size": families[(h.source, h.target)],
            "reverse_present": (h.target, h.source) in families,
            "reverse_lags": sorted(
                lag for (src, dst, lag) in edges
                if src == h.target and dst == h.source
            ),
            "reverse_admitted": False,
            "reverse_admission_claimed_unverified": any(
                other.admitted for (src, dst, _), other in edges.items()
                if src == h.target and dst == h.source
            ),
            "multiplicity_status": "UNVERIFIED",
            "predictive_input": False,
        }
        for h in rows
    ]
