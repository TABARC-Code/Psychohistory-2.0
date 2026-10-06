import numpy as np
from scipy.optimize import minimize

def fit_exponential_hawkes(events,T):
    e=np.sort(np.asarray(events,float))
    if len(e)<5:return {'status':'UNRESOLVED','reason':'need >=5 events'}
    def nll(z):
        mu,alpha,beta=np.exp(z); hist=[]
        for i,ti in enumerate(e): hist.append(mu+alpha*np.exp(-beta*(ti-e[:i])).sum())
        ll=np.log(hist).sum()-mu*T-(alpha/beta)*np.sum(1-np.exp(-beta*(T-e)))
        n=alpha/beta
        return -ll + (1e6*(n>=.999))
    r=minimize(nll,np.log([len(e)/T*.5,.2,1.]),method='Nelder-Mead')
    if not r.success:return {'status':'UNRESOLVED','reason':r.message}
    mu,alpha,beta=np.exp(r.x); n=alpha/beta
    return {'status':'VALID' if n<1 else 'UNRESOLVED','mu':float(mu),'alpha':float(alpha),'beta':float(beta),'branching_ratio':float(n),'log_likelihood':float(-r.fun)}
