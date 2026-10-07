*Feature admission, BOCPD, survival/discrete hazards, PLS and probability calibration*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Temporal semantics
R_d,t=[1(S_d>0), S_d, Delta S_d, Q_d, C_d].
State, momentum, pipeline and cost/pressure semantics remain separate. Positive momentum cannot erase a contractionary state.

# 2. BOCPD
P(r_t,x_1:t)=sum_{r_{t-1}} P(r_t|r_{t-1}) P(x_t|r_{t-1},x^(r)) P(r_{t-1},x_1:t-1).
The parameter is changepoint_rate_prior, not transition hazard. Run-length posterior is a regime diagnostic, not a future-event probability.

# 3. CUSUM/SPRT alternatives
CUSUM: S_t=max(0,S_{t-1}+ell_t-k).
SPRT: Lambda_n=prod_i p_1(x_i)/p_0(x_i); stop when Lambda_n crosses registered bounds.
Alternatives are selected prospectively; repeated detector shopping is multiplicity.

# 4. Stage A sparse-group selection
min_beta L(y,X beta)+lambda_1 sum_g w_g ||beta_g||_2 + lambda_2 ||beta||_1.
Algebraic duplicates are removed before regularisation. Hyperparameters are inner-selected.

# 5. Cox model
h(t|z)=h_0(t) exp(beta^T z).
L_partial(beta)=prod_{i:event} exp(beta^T z_i)/sum_{j in R_i} exp(beta^T z_j).
Cox hazard is statistical, not derived from Itô/OU/spectral equations.

# 6. Discrete-time hazard
logit(q_ik)=alpha_k+beta^T z_ik.
P(event by K)=1-prod_{k=1}^K(1-q_ik).

# 7. PLS projection
PLS is a supervised dimension-reduction candidate. The survival-specific variant and number of components are declared; projection is fitted within each training fold. PCA is not the default.

# 8. Calibration
logit P(Y=1)=alpha+beta logit(p_raw).
Ideal alpha=0,beta=1. Platt/logistic, isotonic and survival-specific calibration compete under nested validation; small samples can make calibration unidentifiable.

# 9. Integrated probability
p_{t,h}=c_h(f_theta(Z_t)); Z_t=Admission(Phi_G1,Phi_G2,Phi_G3,Phi_G23,Sidecars,Anchors,T_E).
No scalarisation is required. The predictor can consume vectors directly.

# 10. Decision theory
a*=argmin_a E[L(a,Y)|F_t].
Warnings require explicit loss/utility. A universal 0.5 threshold is not assumed.

# 11. Forecast issuance
FORECAST(t,contract): reconstruct point-in-time data; validate measurements/ancestry; compute admitted features; obtain baseline predictions; obtain raw PH prediction; calibrate with frozen map; append immutable ledger record before outcome; return probability.