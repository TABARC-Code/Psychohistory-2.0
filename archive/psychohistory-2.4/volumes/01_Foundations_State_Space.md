*Formal foundations and the boundary between mathematics and empirical claims*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Scope and epistemic contract
Psychohistory 2.4 is a forecasting research architecture, not a claimed universal law of history. Mathematical objects below define estimators and tests; they acquire predictive status only through point-in-time held-out or prospective validation.

# 2. Probability space and filtration
(Omega, F, {F_t}_{t>=0}, P)
F_t is the information actually available by forecast origin t. Every production predictor Z_t and issued probability p_{t,h} must be F_t-measurable. Publication after t is future information even when the observation refers to an earlier period.
D_t^(v) = {o_i : availability_i <= t, vintage_i = latest vintage available at t}.

# 3. Canonical latent state
X_t = [M_t, P_t, E_t, I_t, L_t]^T.
The components are conceptual latent fields: narrative/memetic, participation, resources/economics, institutions, and topology/network. They are not assumed mutually independent or directly observable.

## 3.1 General stochastic candidate
dX_t = F(X_t,U_t,Theta) dt + G(X_t,Theta) dW_t + J(X_t,Theta) dN_t.
This is a model family, not an admitted law. F is drift, G diffusion loading, W a multivariate Wiener process, J jump loading and N a counting process. Domain models may omit terms or use discrete-time alternatives.

# 4. Observation system
Y_t = H_t(X_t,C_t,Q_t) + epsilon_t.
p(Y_t|X_t,theta_obs) defines the observation likelihood.

# 5. Forecast operator
D_{<=t}^(v) -> O_t -> T_E -> Phi_G -> A_t -> Z_t -> f_theta -> c -> p(Y_{t:t+h}=1|F_t).
Each arrow is versioned. O is the measurement-valid set, T_E evidence ancestry, Phi_G feature operators, A historical anchors, Z admitted predictors, f_theta the predictive model and c the calibration map.

# 6. Uncertainty
p(p_{t,h}|Y_{<=t}) = integral p(p_{t,h}|X_t,theta) p(X_t,theta|Y_{<=t}) dX_t dtheta.
Exact evaluation is not mandatory; analytic delta methods, bootstrap, posterior simulation or explicit partial/unquantified status are allowed depending on estimator.

# 7. Core principles
- Measurement Validity: an unquantified, unidentified or unvalidated quantity is not yet a measurement.
- Evidence Independence: distinct labels do not imply independent evidence.
- Network Inference: local validity/significance does not imply global discovery.
- Conditional Recurrence: historical resemblance is conditional evidence, never destiny.

# 8. Dimensional and semantic consistency
Transforms cannot upgrade a scale. Every formula that adds or multiplies variables requires compatible or explicitly normalised semantics.

# 9. Identifiability
theta identifiable iff p(Y|theta_1)=p(Y|theta_2) for all Y implies theta_1=theta_2 (within the declared model).
Practical identifiability is assessed by profile likelihood, Hessian/condition diagnostics, simulation recovery, multi-start stability and sensitivity. Optimiser convergence alone is not identification.

# 10. Complete status boundary
The formal specification can be complete while empirical quantities remain unknown. Unknown coefficients, priors, Brier scores, calibration slopes and coupling strengths are deliberately not invented.