def coupling_gate(*,out_of_sample_gain=None,valid_null=False,identifiable=False,multiplicity_corrected=False):
    reasons=[]
    if out_of_sample_gain is None or out_of_sample_gain<=0: reasons.append('no positive held-out gain')
    if not valid_null: reasons.append('null unresolved')
    if not identifiable: reasons.append('weak identifiability')
    if not multiplicity_corrected: reasons.append('multiplicity unresolved')
    return {'status':'ADMITTED' if not reasons else 'TEST_UNRESOLVED','reasons':reasons}
