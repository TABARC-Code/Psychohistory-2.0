from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class ModuleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ZERO_EVIDENCE = "ZERO_EVIDENCE"
    UNAVAILABLE = "UNAVAILABLE"
    INVALID = "INVALID"
    REDUNDANT = "REDUNDANT"
    DEPENDENT = "DEPENDENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    WEAKLY_IDENTIFIED = "WEAKLY_IDENTIFIED"
    UNRESOLVED = "UNRESOLVED"
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"
    ADMITTED = "ADMITTED"


CORE_MODULES = (
    "G1_MEMETICS",
    "G2_STOCHASTIC_STABILITY",
    "G3_NETWORKS",
    "G23_COUPLING",
    "DEPENDENCE_SURROGATES",
    "SEQUENTIAL_DETECTORS",
    "HISTORICAL_ANCHORS",
    "STOCHASTIC_COUNTERMODEL",
)

SIDECARS = (
    "BADL_M",
    "GISC",
    "CTSC",
    "TPSS",
    "IISC",
    "CCSC",
    "SCFS",
)


@dataclass(frozen=True)
class ModuleReport:
    module: str
    status: ModuleStatus
    applicable: bool = True
    evidence_ids: tuple[str, ...] = ()
    horizon: str | None = None
    note: str | None = None


class IncompleteUnifiedRun(RuntimeError):
    pass


def required_modules(extra_modules: Iterable[str] = ()) -> tuple[str, ...]:
    # Stable order is intentional: run manifests should diff cleanly.
    return CORE_MODULES + SIDECARS + tuple(extra_modules)


def validate_unified_run(
    reports: Mapping[str, ModuleReport],
    *,
    extra_modules: Iterable[str] = (),
) -> None:
    """Reject silent module omission.

    This gate does not require every module to agree, be predictive, or have
    evidence. It requires every registered module to report its state.
    """
    required = required_modules(extra_modules)
    missing = [name for name in required if name not in reports]
    if missing:
        raise IncompleteUnifiedRun(
            "Unified Psychohistory run omitted registered modules: "
            + ", ".join(missing)
        )

    for name in required:
        report = reports[name]
        if report.module != name:
            raise IncompleteUnifiedRun(
                f"Report key/module mismatch: {name!r} != {report.module!r}"
            )
        if not report.applicable and report.status != ModuleStatus.NOT_APPLICABLE:
            raise IncompleteUnifiedRun(
                f"{name} is inapplicable but did not report NOT_APPLICABLE"
            )


def disagreement_pairs(
    reports: Mapping[str, ModuleReport],
) -> tuple[tuple[str, str], ...]:
    """Return all independently reported module pairs for downstream comparison.

    Actual distance/comparability is domain-specific and must be computed by
    registered comparison functions; this function deliberately does not
    average or rank module outputs.
    """
    names = sorted(reports)
    return tuple(
        (names[i], names[j])
        for i in range(len(names))
        for j in range(i + 1, len(names))
    )
