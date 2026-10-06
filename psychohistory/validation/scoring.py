def brier(rows):
    if not rows:return {'status':'UNMEASURED','n':0}
    ps=[r[1] for r in rows]; ys=[r[3] for r in rows]; bs=sum((p-y)**2 for p,y in zip(ps,ys))/len(rows)
    base=[r[2] for r in rows if r[2] is not None]
    out={'status':'MEASURED','n':len(rows),'brier':bs}
    if len(base)==len(rows):
        bb=sum((p-y)**2 for p,y in zip(base,ys))/len(rows); out|={'baseline_brier':bb,'brier_skill':None if bb==0 else 1-bs/bb}
    return out
