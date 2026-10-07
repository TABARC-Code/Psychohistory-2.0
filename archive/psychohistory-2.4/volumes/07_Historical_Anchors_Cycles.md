*Trajectory similarity, uncertainty-aware anchors, motifs and counter-anchors*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Anchor
A_t=[S_t,X_t,R_t,E_t,U_t].
A_t^(w)={A_{t-w},...,A_t}.
Only pre-outcome information enters an anchor used for prediction.

# 2. Anchor classes
R recurrence; T transition; F false-positive; N normalisation/recovery; D divergence; C counter-anchor.

# 3. Distance vector
D_A(i,j)=[D_S,D_X,D_R,D_E].
The vector is not collapsed until a weighting rule is prospectively justified.

# 4. Mahalanobis candidate
D_S(i,j)=sqrt((s_i-s_j)^T Sigma_train^{-1}(s_i-s_j)).
Shrinkage/diagonal alternatives apply when covariance is ill-conditioned. Mixed scales require mixed-data metrics.

# 5. Dynamic time warping
D_DTW(X,Y)=min_{pi in Pi} sum_{(a,b)in pi} c(X_a,Y_b)+lambda P(pi).
Warping constraints are frozen; unconstrained warping can erase causally meaningful speed differences.

# 6. Uncertainty-aware distance
Dbar(A_i,A_j)=E[D(A_i*,A_j*)], A_i*~p(A_i|evidence).
U_A=[U_measurement,U_source,U_reconstruction,U_distance,U_outcome,U_sampling].

# 7. Kernel neighbour forecast
phat(Y_{t+h}=1|A_t)= sum_{j in N_k} K(D(A_t,A_j)/b)Y_{j+h} / sum_{j in N_k} K(D(A_t,A_j)/b).
k, bandwidth b and metric are nested-selected. Ordinary kNN is the mandatory baseline.

# 8. Divergence
D_pre(i,j)<<1 and D_post(i,j)>>1 => divergence/counter-anchor candidate.
Failed trajectories identify cycle-breakers and omitted variables.

# 9. Cycle taxonomy
Periodic, quasi-cycle, state recurrence, sequence recurrence, structural recurrence and memetic recurrence are distinct hypotheses.

# 10. Spectral periodicity
I(f)=periodogram/spectral estimate under registered detrending and windowing; Delta f≈1/T_window.
Frequency searches are multiplicity families. Stable phase is not assigned without empirical cyclic structure.

# 11. Quasi-cycles
Stochastic excitation of damped modes must be compared with stochastic linear/nonlinear nulls rather than deterministic periodic fits.

# 12. Conditional recurrence test
Compare P(X_{t+h}|X_{t-w:t}) with P(X_{t+h}|baseline).
Historical resemblance earns predictive status only by improving untouched forecasts.

# 13. Hierarchical atlas
A* = A^M xor A^P xor A^E xor A^I xor A^L (direct-sum concept, not scalar arithmetic).
Domain atlases retain their own scales and uncertainty. Integration is supervised, not averaged by default.