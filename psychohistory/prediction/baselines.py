def base_rate(outcomes):
    if not outcomes:return {'status':'UNMEASURED'}
    return {'status':'VALID','probability':sum(outcomes)/len(outcomes),'n':len(outcomes)}

def persistence(values):
    if not values:return {'status':'UNMEASURED'}
    return {'status':'VALID','prediction':values[-1]}
