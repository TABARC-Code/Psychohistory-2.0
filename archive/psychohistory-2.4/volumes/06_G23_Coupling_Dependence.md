*Master stability, HSIC, distance covariance, surrogates and global inference*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Coupled dynamics
xdot_i=f(x_i;theta_f)+kappa sum_j L_ij H(x_j;theta_H)+epsilon_i.
L=V Gamma V^{-1}; delta X=(V tensor I) eta.
etadot_k=[Df(s)+kappa gamma_k DH(s)] eta_k.

# 2. Master stability function
Lambda(alpha)=limsup_{t->infty}(1/t) log ||eta(t)||, alpha=kappa gamma_k.
transverse stability requires Lambda(kappa gamma_k)<0 for relevant k.
Use requires synchronisation/coupling assumptions; otherwise it is not an admissible model.

# 3. Delayed/time-varying coupling
xdot_i(t)=f(x_i(t))+kappa sum_j L_ij(t) H(x_j(t-tau)).
Delay tau, graph dynamics and kappa can be mutually confounded. Candidate lag selection occurs inside nested validation.

# 4. Identifiability
G23_CPL=[kappahat,U_kappa,Delta L_OOS,Z_CPL,Q_H].
Flat profile likelihood or strong trade-off with intrinsic dynamics/edge scaling => WEAKLY_IDENTIFIED.

# 5. HSIC
H=I-11^T/n; HSIC_b=(1/(n-1)^2) tr(K H L H) [registered normalisation].
Kernel bandwidth is a hyperparameter. Vanilla permutation is invalid under serial dependence.

# 6. Distance covariance
dCov_n^2=(1/n^2) sum_ij A_ij B_ij.
Agreement with HSIC is robustness, not independent replication when based on the same data.

# 7. Surrogate p-value
p=(1+sum_b 1[T_null^b >= T_obs])/(B+1).
Nulls include iAAFT, twin surrogates, block resampling and custom common-driver-preserving surrogates. Invalid null => TEST_UNRESOLVED.

# 8. Multiplicity
BH: sort p_(1)<=...<=p_(m); k=max{i: p_(i)<= i q/m}.
BY replaces q/m threshold with q/(m c_m), c_m=sum_{j=1}^m 1/j, for arbitrary dependence control.
Hierarchical/online FDR may be used where registered. Lifetime denominators are not reset after negative results.

# 9. Status ladder
OBSERVED -> STATISTICALLY DEPENDENT -> FDR-SURVIVING CANDIDATE -> REPLICATED RELATIONSHIP -> MECHANISTICALLY SUPPORTED -> ADMITTED PREDICTIVE EVIDENCE.

# 10. G23 test
Freeze f,H,graph scaling,lag family; fit intrinsic and coupled models; profile kappa/H; compare inner-validation predictive loss; run common-driver preserving surrogate; multiplicity-correct family; outer-test once; promote only with incremental skill.