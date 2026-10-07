*Laplacian fragmentation, covariance crowding, exposure graphs and perturbation bounds*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Graph objects
G_t=(V_t,E_t,W_t); D_ii=sum_j W_ij.
L=D-W; L_sym=I-D^{-1/2} W D^{-1/2}.
Operator choice is part of the feature definition. There is no universal lambda_1.

# 2. Fragmentation
0=lambda_1 <= lambda_2 <= ...; connected undirected graph => lambda_2>0.
lambda_2 is algebraic connectivity under the chosen Laplacian. Graph size, density and scaling must be controlled.

# 3. Fiedler rotation
R_t=1-|v_2(t)^T v_2(t-Delta)|.
Absolute inner product removes sign indeterminacy. Near lambda_2≈lambda_3 the vector is unstable.

# 4. Weyl bound
|lambda_k(A+E)-lambda_k(A)| <= ||E||_2.

# 5. Davis-Kahan
||sin Theta(V,Vhat)|| <= ||E||_2/delta.
A spectral change below plausible graph-construction perturbation is not resolved.

# 6. Covariance crowding
S=(1/(T-1)) X^T X (after registered centring/scaling).
q=N/T; lambda_pm=sigma^2(1 +/- sqrt(q))^2 [Marchenko-Pastur iid reference].
Serial dependence and heteroskedasticity generally require stronger nulls. BBP-style separation is a detectability concept, not a universal transition criterion.

# 7. Effective rank candidate
p_i=lambda_i/sum_j lambda_j; r_eff=exp(-sum_i p_i log p_i).
Descriptive only; does not replace evidence ancestry.

# 8. Exposure graph
G_X(t)={V_X,E_X,W_X}; G_R(t)={V_R,E_R,W_R}.
Exposure and response are separate graphs. Physical/network distance D_L differs from geographic distance D_G.

# 9. Edge uncertainty
What_ij = W_ij + E_ij; propagate E through eigen/spectral statistics.
Missing edges and zero edges are distinct. Coverage is part of graph vintage.

# 10. Dynamic graphs
W=W(t), L=L(t).
Node-set changes require a common-node panel or validated changing-node normalisation. Silent dimensional drift is prohibited.

# 11. Network nulls
GRAPH_NULL(feature): preserve node strengths/degrees as required; temporal autocorrelation; common drivers; destroy only hypothesised structure. If no defensible null: TEST_UNRESOLVED.