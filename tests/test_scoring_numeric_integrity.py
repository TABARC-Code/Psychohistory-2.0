"""Arithmetic integrity only; these are not matured empirical forecasts."""
import pytest

from psychohistory.validation.scoring import brier


def test_known_brier_and_skill_remain_correct():
    result = brier([('a', .2, .4, 0), ('b', .8, .6, 1)])
    assert result['status'] == 'MEASURED'
    assert result['brier'] == pytest.approx(.04)
    assert result['baseline_brier'] == pytest.approx(.16)
    assert result['brier_skill'] == pytest.approx(.75)
    assert result['validation_scope'] == 'ARITHMETIC_ONLY'
    assert result['predictive_input'] is False


def test_empty_ledger_is_unmeasured():
    assert brier([])['status'] == 'UNMEASURED'


@pytest.mark.parametrize('bad', [
    ('a', float('nan'), .5, 1),
    ('a', float('inf'), .5, 1),
    ('a', -0.1, .5, 1),
    ('a', 1.4, .5, 1),
    ('a', True, .5, 1),
    ('a', 10**400, .5, 1),
    ('a', .3, float('nan'), 1),
    ('a', .3, -0.1, 1),
    ('a', .3, 2.0, 1),
    ('a', .3, .5, 0.3),
    ('a', .3, .5, True),
    ('a', .3, .5, 2),
    ('a', .3, .5, '1'),
    ('', .3, .5, 1),
    (1, .3, .5, 1),
    ('a', .3, .5),
])
def test_invalid_rows_never_claim_measured(bad):
    result = brier([bad])
    assert result['status'] == 'UNRESOLVED'
    assert result['n'] == 0
    assert 'brier' not in result


def test_duplicate_forecast_ids_do_not_count_twice():
    result = brier([('a', .9, .5, 1), ('a', .9, .5, 1)])
    assert result['status'] == 'UNRESOLVED'
    assert result['n'] == 0


def test_partial_baseline_does_not_generate_skill():
    result = brier([('a', .2, None, 0), ('b', .8, .6, 1)])
    assert result['status'] == 'MEASURED'
    assert 'brier_skill' not in result


def test_perfect_baseline_has_undefined_skill():
    result = brier([('a', .5, 0, 0), ('b', .5, 1, 1)])
    assert result['status'] == 'MEASURED'
    assert result['baseline_brier'] == 0
    assert result['brier_skill'] is None


def test_extreme_valid_probability_ratio_does_not_emit_infinite_skill():
    result = brier([('a', 1., 1e-200, 0)])
    assert result['status'] == 'MEASURED'
    assert result['baseline_brier'] == 0.0
    assert result['brier_skill'] is None


def test_generators_supported_without_changing_score():
    result = brier(row for row in [('a', .2, .4, 0), ('b', .8, .6, 1)])
    assert result['status'] == 'MEASURED'
    assert result['n'] == 2


def test_no_independent_provenance_is_inferred():
    result = brier([('a', .1, .5, 0)])
    assert result['validation_scope'] == 'ARITHMETIC_ONLY'
    assert result['predictive_input'] is False


def test_duplicate_rows_cannot_reverse_reported_skill():
    unique = [('A', .9, .5, 1), ('B', .9, .5, 0)]
    duplicate = [unique[0]] * 10 + [unique[1]]
    assert brier(unique)['brier_skill'] == pytest.approx(-.64)
    assert brier(duplicate)['status'] == 'UNRESOLVED'


def test_nonzero_subnormal_baseline_never_emits_infinite_skill():
    result = brier([('a', 1., 1e-160, 0)])
    assert result['status'] == 'MEASURED'
    assert 0 < result['baseline_brier'] < 1e-300
    assert result['brier_skill'] is None
