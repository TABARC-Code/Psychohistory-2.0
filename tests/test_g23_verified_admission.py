from math import inf, nan
from psychohistory.g23.gate import coupling_gate


def test_all_caller_assertions_cannot_admit():
    r = coupling_gate(out_of_sample_gain=0.1, valid_null=True,
                      identifiable=True, multiplicity_corrected=True)
    assert r['status'] == 'TEST_UNRESOLVED'
    assert r['candidate_numerically_eligible'] is True
    assert r['provenance_status'] == 'UNVERIFIED'
    assert r['predictive_input'] is False
    assert any('provenance' in s for s in r['reasons'])


def test_invalid_numerical_claims_still_rejected():
    for gain in (None, True, 0, -1, nan, inf, -inf):
        r = coupling_gate(out_of_sample_gain=gain, valid_null=True,
                          identifiable=True, multiplicity_corrected=True)
        assert r['status'] != 'ADMITTED'
        assert r['candidate_numerically_eligible'] is False
        assert 'no finite positive held-out gain' in r['reasons']


def test_truthy_nonboolean_flags_not_verified():
    for key in ('valid_null', 'identifiable', 'multiplicity_corrected'):
        flags = {'valid_null': True, 'identifiable': True, 'multiplicity_corrected': True}
        flags[key] = 'true'
        r = coupling_gate(out_of_sample_gain=0.2, **flags)
        assert r['candidate_numerically_eligible'] is False
        assert r['status'] == 'TEST_UNRESOLVED'


def test_no_implicit_admission_when_gain_extreme():
    r = coupling_gate(out_of_sample_gain=1e300, valid_null=True,
                      identifiable=True, multiplicity_corrected=True)
    assert r['candidate_numerically_eligible'] is True
    assert r['status'] == 'TEST_UNRESOLVED'
