import numpy as np
import pytest
from psychohistory.g1.hawkes import fit_exponential_hawkes

@pytest.mark.parametrize('seed',range(8))
def test_unit_invariance_of_hawkes_fit(seed):
    e=np.sort(np.random.default_rng(seed).uniform(0,100,15))
    ref=fit_exponential_hawkes(e,100)
    assert ref['status'] in ('VALID','UNRESOLVED')
    for scale in (1e-6,1e-3,1e3,1e6):
        got=fit_exponential_hawkes(e*scale,100*scale)
        assert got['status']==ref['status']
        assert got['predictive_input'] is False
        if got['status']=='VALID':
            assert got['branching_ratio']==pytest.approx(ref['branching_ratio'],abs=1e-6)
            for rate in ('mu','alpha','beta'):
                assert got[rate]*scale==pytest.approx(ref[rate],rel=1e-5)
            assert got['log_likelihood']==pytest.approx(
                ref['log_likelihood']-len(e)*np.log(scale),abs=1e-5)
        elif 'branching_ratio_candidate' in ref:
            assert got['branching_ratio_candidate']==pytest.approx(
                ref['branching_ratio_candidate'],abs=1e-6)

@pytest.mark.parametrize('events,T',[
    ([1,2,3,4,11],10),([1,1,2,3,4,5],10),([1,2,3,4,5],0),
    ([1,2,3,4,float('nan')],10),([1,2,3,4,float('inf')],10),
])
def test_invalid_windows_fail_closed(events,T):
    assert fit_exponential_hawkes(events,T)['status']=='UNRESOLVED'

def test_regular_event_history_near_zero_excitation_not_identified():
    result=fit_exponential_hawkes(np.linspace(1,9,9),10)
    assert result['status']=='UNRESOLVED'
    assert result['predictive_input'] is False
