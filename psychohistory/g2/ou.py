import numpy as np
from scipy.optimize import minimize

def fit_ou(times, values):
    t=np.asarray(times,float); x=np.asarray(values,float)
    if len(x)<4: return {'status':'UNRESOLVED','reason':'need >=4 observations'}
    dt=np.diff(t); prev=x[:-1]; nxt=x[1:]
    def nll(z):
        a=np.exp(z[0]); mu=z[1]; sigma=np.exp(z[2]); e=np.exp(-a*dt); m=mu+(prev-mu)*e; v=sigma*sigma/(2*a)*(1-e*e)
        return .5*np.sum(np.log(2*np.pi*v)+(nxt-m)**2/v)
    z0=[np.log(.1),float(np.mean(x)),np.log(max(np.std(x),1e-6))]; r=minimize(nll,z0,method='L-BFGS-B')
    if not r.success:return {'status':'UNRESOLVED','reason':r.message}
    a,mu,sigma=np.exp(r.x[0]),r.x[1],np.exp(r.x[2])
    return {'status':'VALID','a':float(a),'mu':float(mu),'sigma':float(sigma),'recovery_time':float(1/a),'log_likelihood':float(-r.fun),'boundary_warning':bool(a<1e-4)}
