*OU inference, critical transitions, Hopf, flickering and non-normal dynamics*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. OU process
dX_t=-a(X_t-mu)dt+sigma dB_t, a>0.
X_{t+Delta}=mu+(X_t-mu)e^{-aDelta}+sigma integral_t^{t+Delta} e^{-a(t+Delta-s)}dB_s.
m_i=mu+(X_i-mu)e^{-aDelta_i}; V_i=sigma^2(1-e^{-2aDelta_i})/(2a).
ell=-1/2 sum_i[log(2pi V_i)+(X_{i+1}-m_i)^2/V_i].

# 2. Stationary identities
Var(X)=sigma^2/(2a); Corr(X_t,X_{t+Delta})=e^{-aDelta}; recovery_time=1/a.
These are derived from the same parameters and therefore not independent features.

# 3. Diagnostics
D_V=V_emp-sigmahat^2/(2 ahat).
D_rho=rho_emp(Delta)-exp(-ahat Delta).
Uncertainty includes parameter covariance; near a=0 bootstrap/profile methods dominate delta approximations.

# 4. Observation-noise extension
dX_t=-a(X_t-mu)dt+sigma dB_t; Y_t=X_t+epsilon_t, epsilon_t~N(0,tau^2).
Kalman/state-space likelihood is a candidate when measurement noise is material. tau and sigma may be weakly identifiable at low sampling frequency.

# 5. Saddle-node normal form
dx/dt = r - x^2 + eta(t) (local canonical candidate).
Critical slowing is mechanism-dependent. Rising variance or autocorrelation alone is not sufficient.

# 6. Hopf normal form
dz/dt=(lambda+i omega)z-(c+i d)|z|^2 z + noise.
Hopf-compatible approach: Re(lambda_pair)->0 with Im(lambda_pair)!=0.
frequency resolution approximately Delta f >= 1/T_window.
Without sufficient window length the oscillatory claim is unresolved.

# 7. Flickering
P(S_t=j|S_{t-1}=i)=P_ij; Y_t|S_t=k ~ emission_k(theta_k).
Hidden-state switching is a candidate representation. Regime number and emissions are selected inside nested validation.

# 8. Non-normal amplification
xdot=A x; asymptotic stability: max Re eig(A)<0.
G(t)=||exp(A t)||_2; G_max=sup_{t>=0} G(t).
G_max>1 can occur despite asymptotic stability. Transient amplification is routed to alternative-process evidence, not critical-transition evidence.

# 9. Pseudospectrum
Lambda_epsilon(A)={z: ||(zI-A)^{-1}|| > 1/epsilon}.
Large pseudospectral excursions can reveal sensitivity hidden by eigenvalues. Numerical resolution and model uncertainty must be included.

# 10. Model-departure router
ROUTE_G2(departure): test transition-consistent signatures; alternative process families; generic misspecification. If signatures non-identifiable: UNRESOLVED; else emit diagnostic + uncertainty + routing action.