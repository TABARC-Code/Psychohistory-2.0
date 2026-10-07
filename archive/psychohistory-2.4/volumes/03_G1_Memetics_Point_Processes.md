*Diffusions, jumps, Hawkes processes, contagion, source trees and mutation*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Diffusion benchmark
dX_t=mu(X_t,t;theta_mu)dt+sigma(X_t,t;theta_sigma)dB_t.
Delta X_i approx Normal(mu_i Delta_i, sigma_i^2 Delta_i).

# 2. Itô transform
df=(partial_t f + mu partial_x f + 1/2 sigma^2 partial_xx f)dt + sigma partial_x f dB_t.
Used for stochastic transformations, not to derive the transition hazard.

# 3. Jump diffusion
dX_t=mu_t dt+sigma_t dB_t+J_t dN_t.
RV=sum r_i^2 -> integral sigma_s^2 ds + sum jumps^2.
BV approx (pi/2) sum_{i=2}^n |r_i||r_{i-1}|.

# 4. Univariate Hawkes
lambda(t)=mu+sum_{t_i<t} alpha exp[-beta(t-t_i)].
ell(mu,alpha,beta)=sum_i log lambda(t_i)-mu T-(alpha/beta)sum_i[1-exp(-beta(T-t_i))].
n=alpha/beta. Stationary branching interpretation requires n<1.

# 5. Time rescaling
Lambda(t)=integral_0^t lambda(s)ds; z_i=Lambda(t_i)-Lambda(t_{i-1}); u_i=1-exp(-z_i).
Correct conditional intensity implies transformed u_i approximately iid Uniform(0,1); both marginal and serial diagnostics are required.

# 6. Multivariate Hawkes
lambda_k(t)=mu_k+sum_j sum_{t_i^j<t} alpha_kj exp[-beta_kj(t-t_i^j)].
A*_kj=alpha_kj/beta_kj; stationarity requires spectral_radius(A*)<1.
Cross-excitation is predictive structure, not causal proof; common broadcaster hypotheses remain competitors.

# 7. Contagion families
P_simple(adopt|k)=1-(1-p)^k.
P_complex(adopt)=f(k_independent,w_ties,theta,context).
lambda_j(t)=baseline_j(t)+broadcast_j(t)+peer_excitation_j(t).

# 8. Propagation kernel
K_M(i,j,Delta t)=P(j receives/adopts M | i,Delta t,C,L,I).
R_observed=f(M,C,L,P,I).
Meme and carrier are separated: M x Carrier. Carrier affects reach, latency, fidelity, mutation and topology.

# 9. Source-tree posterior
P(S,T_S|O,C,L) proportional to P(O|S,T_S,C,L) P(T_S|S,L,C) P(S).
Competing hypotheses: single source, independent sources, common broadcaster, coordinated activity, observation artefact. Coordinated activity does not imply intent.

# 10. Source entropy
U_S=-sum_s p_s log p_s.
High source entropy means uncertainty, not distributed ignition.

# 11. Genealogy and mutation
P(parent=j|child=i) proportional to 1[t_j<t_i] K_M(j,i,Delta t) exp[-eta d(m_i,m_j)].
Descendants share ancestry and cannot be counted as independent evidence. Semantic metrics must be frozen without future-corpus leakage.

# 12. Influence
Influence_{M->R}(h) := incremental predictive information of M_t for R_{t:t+h} conditional on baseline B_t.
Virality, systemic influence and transition are distinct.

# 13. G1 process selector
G1_SELECTOR(series/events): validate observation process; fit null/baseline; fit diffusion/jump/count candidates as admissible; diagnose residuals; nested-compare predictive score; correct model-family search; return selected family or PROCESS_UNRESOLVED.