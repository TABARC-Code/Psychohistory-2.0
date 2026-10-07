import pytest

from psychohistory.core.unified import (
    CORE_MODULES,
    SIDECARS,
    IncompleteUnifiedRun,
    ModuleReport,
    ModuleStatus,
    disagreement_pairs,
    validate_unified_run,
)


def _complete_reports():
    return {
        name: ModuleReport(name, ModuleStatus.ZERO_EVIDENCE)
        for name in CORE_MODULES + SIDECARS
    }


def test_unified_run_requires_every_registered_module():
    reports = _complete_reports()
    reports.pop("IISC")
    with pytest.raises(IncompleteUnifiedRun):
        validate_unified_run(reports)


def test_null_evidence_is_valid_but_silent_omission_is_not():
    validate_unified_run(_complete_reports())


def test_inapplicable_module_must_say_so():
    reports = _complete_reports()
    reports["CTSC"] = ModuleReport(
        "CTSC", ModuleStatus.ZERO_EVIDENCE, applicable=False
    )
    with pytest.raises(IncompleteUnifiedRun):
        validate_unified_run(reports)


def test_disagreement_layer_preserves_pairs():
    reports = _complete_reports()
    pairs = disagreement_pairs(reports)
    assert ("BADL_M", "GISC") in pairs
    assert ("G1_MEMETICS", "STOCHASTIC_COUNTERMODEL") in pairs
