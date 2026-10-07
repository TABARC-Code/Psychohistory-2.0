# Psychohistory 2.4 — Full Technical Paper

> Recovered text export of the canonical 2026-10-06 DOCX held in the ChatGPT project Library. The source DOCX SHA-256 is `16287e5a4e5406dd43588632a8e5fe6c15829e4c954ca7530b26e748d9637903`; canonical PDF SHA-256 is `0dab25a2f1fecebdac9a3e361c643615fb24ce4e6aecd9c33a6a337df76b37e4`. This UTF-8 export is provided for repository inspection; the binary originals remain canonical.

<PARSED TEXT FOR PAGE: 1 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
Psychohistory 2.4
A leakage-resistant framework for conditional recurrence, memetic propagation,
network transition inference and prospective complex-system forecasting
Technical specification and research paper — storage edition — 6 October 2026
Status: research architecture. Psychohistory 2.4 does not presently have a demonstrated aggregate out￾of-sample Brier score, calibration slope, false-alert rate, or lead-time advantage. This document 
therefore separates mathematical specification, candidate machinery, development evidence, and 
validated predictive evidence throughout.
This storage edition consolidates the complete framework developed to date. It is intended to be 
sufficient to reconstruct an implementation without relying on the conversational history. Algorithms 
are given explicitly; unresolved quantities remain unresolved rather than being filled with invented 
coefficients or retrospective performance claims.
Abstract
Psychohistory 2.4 is a research framework for forecasting transitions in complex social, economic, 
institutional, technological and narrative systems. Its central claim is deliberately narrower than 
fictional psychohistory: partially recurrent system states, propagation structures and transition motifs 
may contain predictive information when they are measured point-in-time, compared against simple 
baselines and tested without future leakage. The framework combines stochastic-process diagnostics, 
narrative and memetic propagation, local-stability estimation, network topology, optional coupling 
models, historical anchor retrieval, domain sidecars, sequential change detection and survival-style 
transition calibration. It treats measurement validity, evidence independence and network inference as 
constitutional constraints rather than optional statistical hygiene.
The architecture is designed to fail safely. Algebraically derived quantities cannot masquerade as 
independent evidence; multiple transforms of one series retain common ancestry; current state is 
separated from future hazard; shocks are separated from exposure; publication lead is separated from 
phenomenon lead; current, pipeline and expectation measures retain horizon semantics; network edges
are validated locally rather than inferred from an attractive causal story; and every prospective claim 
requires a frozen outcome contract, information set and forecast ledger entry. Historical resemblance is
conditional evidence, never destiny. The present document specifies the full algorithms but records no 
aggregate predictive success because the required prospective lockbox has not yet matured.
1. Research question and scope
The research question is whether a heterogeneous complex system can be represented in a sufficiently 
disciplined state space that recurring configurations, propagation motifs and local instabilities improve 
forecasts of defined transitions beyond conventional baselines. The framework is not permitted to 
answer this by retrospective storytelling. It must beat base rates, persistence, simple time-series models 
<PARSED TEXT FOR PAGE: 2 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
and any recognised leading indicators it consumes, using only information genuinely available at each 
forecast origin.
The canonical latent state is X_t = [M_t, P_t, E_t, I_t, L_t], where M denotes narrative or memetic state, P 
participation and mobilisation, E resources and economic conditions, I institutional state, and L 
topology or network structure. These fields are conceptual containers rather than automatically 
estimated scalar factors. A field may remain multivariate when reduction would destroy identified 
information.
Field Meaning
Examples of 
admissible 
observations
Prohibited shortcut
M Narrative/memetic 
field
message frequency, 
mutation lineage, 
diffusion structure, 
source posterior
single sentiment score 
treated as social reality
P Participation turnout, adoption, 
transaction 
participation, 
mobilisation
raw counts without 
denominator/exposure
E Resources/economics prices, credit, output, 
flows, buffers
generic 'economic 
stress' scalar without 
identification
I Institutions capacity, legitimacy 
proxies, policy 
response, rule changes
intent inferred from 
outcome
L Topology/network Laplacian, covariance, 
exposure graph, 
communication graph
one universal 
eigenvalue used for 
every network
2. Constitutional principles
2.1 Measurement Validity
An unquantified, unidentified or unvalidated quantity is not yet a measurement. Every production 
variable requires an observation model, units or scale semantics, uncertainty, point-in-time 
provenance, an identifiability assessment and a declared role. Attractive names do not create 
measurable constructs.
2.2 Evidence Independence
Distinct labels do not imply independent evidence. Shared source data, shared transformations, 
common causal ancestry, nested geography, repeated releases and derived indicators are represented 
in an Evidence Ancestry Graph. Informational breadth is never allowed to exceed the number of 
defensible independent evidence paths.
<PARSED TEXT FOR PAGE: 3 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
2.3 Network Inference
A locally valid or statistically significant relationship is not automatically a globally valid discovery. 
Each network edge, lag and mechanism must be tested under an appropriate null, multiplicity family 
and point-in-time information set. Evidence for A B does not validate B C. → →
2.4 Conditional Recurrence
Historical systems may enter partially similar states, but resemblance is conditional evidence rather 
than determinism. Historical anchors must use only pre-outcome information, preserve observation 
uncertainty and include false-positive, normalisation and divergence cases. An anchor contributes only 
if it improves untouched predictive performance over simpler alternatives.
3. Information architecture and data contracts
3.1 Observation record
ObservationRecord:
 observation_id
 variable_id
 domain
 entity_or_geography
 reference_start
 reference_end
 publication_time
 availability_time
 source_uri
 source_version
 method_version
 raw_value
 units
 scale_semantics
 revision_status
 information_maturity
 sample_composition
 known_defects
 current_state_horizon
 forecast_horizon_if_any
 ancestry_parent_ids[]
 uncertainty
 quality_flags[]
<PARSED TEXT FOR PAGE: 4 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
Publication time and reference time are separate. A release may arrive early while measuring a 
contemporaneous or already elapsed phenomenon; such a release has publication lead but not 
necessarily phenomenon lead. Information maturity records whether a release is based on incomplete 
underlying records, a flash sample, a scheduled revision or a finalised source. Revision provenance 
distinguishes scheduled revision, incomplete-data maturation, methodological revision and explicit 
correction.
3.2 Derived-feature vintage integrity
Every derived feature must be reconstructed from the component vintages available at the forecast 
origin. If G is a network construction operator, then Network_t^forecast = G(X_1t^v, …, X_nt^v), where 
every superscript v denotes the version visible at t. Recomputing a historical network with today's 
revised component data is future leakage.
3.3 Scale semantics
A transformation cannot confer stronger measurement semantics than its source. For example, PMI 50 −
is a diffusion-index displacement, not a direct output-growth magnitude. MoM, YoY, z-scores and 
deviations from averages are alternative representations of a common series unless held-out evidence 
establishes incremental information.
3.4 Horizon semantics
Current state, momentum, pipeline and expectations must remain distinguishable. Indicators sharing a 
publication month are not automatically observations of the same temporal state. A new-orders 
measure can be a leading pipeline variable; a current-output measure is contemporaneous; an 
expectations survey is a subjective future distribution. Claimed lead time must be measured relative to 
the corresponding recognised leading-indicator baseline, not merely relative to the final outcome date.
3.5 Shock-exposure separation
A shock and the population's exposure to that shock are separate quantities. A useful generic 
representation is Exposure_i,t = Price_t × Quantity_i,t × Dependency_i,t, with buffers, contracts, hedges 
and substitution modifying transmission. National prices cannot be converted directly into 
homogeneous behavioural impact.
4. Evidence ancestry and hypothesis accounting
4.1 Evidence Ancestry Graph
The Evidence Ancestry Graph T_E is a directed provenance graph. It records plausible shared 
observational and transformation ancestry; it is not itself a causal graph.
BUILD_EVIDENCE_ANCESTRY(observations, transforms):
 create directed graph T_E
 for each raw observation o:
 add node(o.id, type="raw", source=o.source_version)
 for each derived feature f:
 add node(f.id, type="derived", transform=f.transform_id)
 for parent in f.parent_ids:
<PARSED TEXT FOR PAGE: 5 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 add edge(parent, f.id, relation="derives")
 for observations sharing sampling frame, release system, nested geography,
 survey respondents, or known common upstream source:
 add typed ancestry links
 compute ancestry clusters only for evidence-accounting purposes
 return T_E
4.2 Informational breadth
Observed breadth is a count of indicators or locations. Informational breadth is the number of 
defensible, non-redundant evidence paths after ancestry adjustment. It satisfies Breadth_informational 
≤ Breadth_observed. The framework does not currently prescribe a universal numerical estimator for 
informational breadth; any such estimator remains a candidate requiring calibration.
4.3 Hypothesis registry and multiplicity
HypothesisRecord:
 hypothesis_id
 origin_time
 variables[]
 direction_if_declared
 lag_candidates[]
 scale_candidates[]
 outcome_contract_id
 null_model_id
 multiplicity_family
 test_statistic
 raw_p
 adjusted_q
 replication_status
 predictive_input = false by default
 status
Benjamini-Hochberg FDR is the default within defensible families; Benjamini-Yekutieli is a fallback 
under arbitrary dependence. Hierarchical FDR may be used where hypotheses have a declared tree. 
Continuous research requires online FDR or alpha-wealth accounting; the denominator cannot be reset 
whenever a new analysis begins.
The status ladder is OBSERVED STATISTICALLY DEPENDENT FDR-SURVIVING CANDIDATE → → →
REPLICATED RELATIONSHIP MECHANISTICALLY SUPPORTED ADMITTED PREDICTIVE EVIDENCE. → →
Advancement requires explicit evidence; labels do not advance automatically.
<PARSED TEXT FOR PAGE: 6 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
5. G1: narrative and memetic dynamics
5.1 Process dispatch
Narrative series cannot be assumed differentiable. Brownian-like paths are non-differentiable and 
bursty media processes may contain jumps or self-excitation. G1 therefore begins with process-family 
selection rather than computing raw narrative acceleration.
G1_PROCESS_DISPATCH(series, timestamps, preregistered_candidates):
 validate observation process and missingness
 fit candidate families inside training data only:
 diffusion_or_drift
 jump_diffusion
 Hawkes_self_exciting
 count_model_with_exogenous_forcing
 narrative_null
 score candidates using nested predictive likelihood and diagnostics
 if no family is identifiable:
 return TEST_UNRESOLVED
 return selected_family, uncertainty, diagnostic_bundle
5.2 Diffusion and jump diagnostics
The generic stochastic representation is dX = μ(X,t)dt + σ(X,t)dB. Itô's formula is retained for 
transformation and stochastic-feature reasoning. Realised quadratic variation may mix continuous 
variance and jumps, so jump-robust bipower or truncated measures are required when the observation
process supports them.
5.3 Hawkes dynamics
For event times t_i, a basic exponential Hawkes process uses λ(t)=μ+Σ_{t_i<t} α exp[-β(t t_i)]. The −
branching ratio n=α/β is derived from fitted α and β and cannot enter the model as an independent 
feature. Near n=1, uncertainty and boundary behaviour require bootstrap or profile methods rather 
than naïve Gaussian approximations.
5.4 Meme and carrier separation
A meme is represented by propagation behaviour rather than carrier technology. Meme Carrier ⊗
separates semantic/narrative content from the medium that controls reach, speed, fidelity, mutation 
and topology. Medieval preaching, pamphlets, broadcast media and social networks may share 
contagion families without being treated as identical systems.
The propagation kernel is K_M(i,j,Δt)=P(j receives or adopts M | i, Δt, C, L, I). Physical distance and 
network distance are explicitly different: D_G ≠ D_L.
5.5 Source-tree inference
Single-source inference is insufficient for historical and modern cascades. The target is P(S_0,T_S | O), 
where S_0 is a set of candidate sources and T_S a source/propagation tree. Competing hypotheses 
include single-source cascade, independent sources, common broadcaster, coordinated activation and 
<PARSED TEXT FOR PAGE: 7 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
observation artefact. The neutral production label is coordinated_activity; behavioural patterns do not 
imply intent.
INFER_SOURCE_TREE(observations, network, carrier, candidate_sources):
 define H1 single_source_cascade
 define H2 independent_sources
 define H3 common_broadcaster
 define H4 coordinated_activity
 define H5 observation_artifact
 construct likelihood under each hypothesis using point-in-time network
 include source and observation uncertainty
 estimate posterior model probabilities
 if posterior separation is weak:
 report SOURCE_UNRESOLVED
 return posterior_over_hypotheses, posterior_over_sources_and_trees
5.6 Contagion families
The selector C_M {simple, complex, broadcast, hybrid}. A simple-contagion benchmark may use ∈
P(adopt|k)=1 (1 p)^k. Complex contagion uses a function of independent exposures, tie weights and − −
threshold θ. The conceptual memetic reproduction potential R_M* is not admitted until an identifiable 
estimator exists.
5.7 Mutation and genealogy
Narrative descendants are represented as lineages M_0 M_1 M_2 with branching where necessary. → →
Descendant observations cannot count as independent confirmations of the ancestor. G1 is therefore 
split conceptually into G1^D dynamics, G1^S source/source-tree, G1^G genealogy/mutation and G1^I 
downstream influence.
5.8 Historical normalisation
Cross-era comparison may use a medium-relative time coordinate τ_M=(t t_0)/T_medium, but −
normalisation cannot remove the causal role of carrier structure. Historical observation is O_historical 
= S(M_historical)+ε, where S is the archival selection process. Every historical anchor therefore carries 
Q_A^OBS for survivorship, recording and reconstruction quality.
6. G2: local stability and critical-transition diagnostics
6.1 Ornstein-Uhlenbeck local model
The canonical local-stability benchmark is dX= aXdt+σdB. Under stationarity, Var(X)=σ²/(2a), lag −
autocorrelation at Δ is exp( aΔ), and recovery time is 1/a. These are algebraically related; if a and σ² are −
fitted, variance and autocorrelation expectations cannot be counted as independent predictive features.
The free parameters are [â, σ̂²]. Independent empirical diagnostics include D_V = V_emp − σ̂²/(2â) and 
D_ρ = ρ_emp(Δ) exp( âΔ). − −
<PARSED TEXT FOR PAGE: 8 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
6.2 Diagnostic uncertainty
Every diagnostic includes uncertainty and an identifiability flag. For D_ρ, delta-method variance must 
include covariance among fitted quantities; near the boundary a 0, bootstrap inference is primary. A →
naked residual cannot enter the classifier.
DIAGNOSTIC_CONTRACT:
 name
 observed_statistic
 model_expected_value
 discrepancy
 uncertainty
 resolution_bound
 identifiable
 transition_signature
 routing_action
6.3 Model departure routing
Q_departure is partitioned into Q_transition, Q_alternative_process and Q_generic_misfit. Transition￾consistent patterns include saddle-node critical slowing, flickering and properly identified Hopf 
behaviour. Alternative processes include non-normal transient amplification, exogenous forcing, 
heteroskedasticity, topology sampling error and model-family mismatch. Generic misspecification 
reduces confidence rather than being rebranded as transition evidence.
6.4 Hopf and spectral resolution
A Hopf claim requires complex eigenvalues approaching Re=0 together with resolvable narrow-band 
periodicity. Frequency resolution is approximately Δf 1/T_window. No spectral claim is admitted ≈
without a resolution bound.
7. G3: topology and network structure
There is no universal λ1. Spectral quantities are operator-specific and their meanings must be 
preserved.
Module Operator Primary interpretation
G3-L Graph Laplacian fragmentation/connectivity
G3-C Covariance/correlation operator crowding/common modes
G3-A Adjacency/exposure operator propagation/exposure
7.1 Laplacian fragmentation
For the graph Laplacian, λ1=0 for a connected component under standard ordering and algebraic 
connectivity is λ2. Declining λ2 toward zero can indicate fragmentation. Fiedler-vector rotation may be 
measured as 1 |<v_t,v_{t Δ}>|. Davis-Kahan bounds are used for eigenvector perturbation and Weyl- − −
type bounds for eigenvalue uncertainty.
<PARSED TEXT FOR PAGE: 9 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
7.2 Covariance crowding
Random-matrix theory and BBP-style separation may be used where sampling assumptions are 
approximately defensible. Dyson eigenvalue repulsion is a null concept, not a universal phase-transition
criterion.
7.3 Exposure propagation
Adjacency or weighted exposure matrices represent pathways through which shocks may propagate. 
Their dominant modes have different semantics from Laplacian connectivity and covariance crowding. 
G3-J was deleted because it duplicated G2 spectral-abscissa information and must not be reintroduced 
under a new label.
8. G23: conditional coupling between stability and topology
G2 and G3-L may interact under diffusive coupling. A generic master-stability representation is 
xdot_i=f(x_i)+κΣ_j L_ij H(x_j), with modal dynamics ηdot_k=[Df(s)+κγ_k DH(s)]η_k. This machinery is 
production-eligible only if a coupling contract passes.
G23_COUPLING_CONTRACT(data, graph_vintages, candidate_H, lag_set):
 require declared coupling family H
 require scale normalisation
 require sufficient independent modes to identify kappa and H parameters
 declare candidate lags before outer evaluation
 embargo E >= maximum effective lookback of every parent feature
 fit inside nested training folds
 compare predictive loss with and without coupling
 test against registered surrogate nulls
 output [kappa_hat, U_kappa, DeltaLoss_OOS, Z_CPL, Q_H]
 if null invalid or identifiability fails:
 return TEST_UNRESOLVED
8.1 Surrogate registry
Permissible null generators include iAAFT, twin surrogates, block resampling and custom multivariate 
common-driver-preserving surrogates. The null must preserve the nuisance structure relevant to the 
hypothesis. An invalid null yields TEST_UNRESOLVED, not significance.
For B surrogate replicates, an empirical add-one p-value is p=[1+Σ_b 1(ΔL_null^b ΔL_obs)]/(B+1). ≥
Predictive coupling is not causal proof.
9. Model-free dependence
HSIC is the default model-free dependence statistic and distance covariance is a corroborating 
alternative. Serially dependent observations invalidate vanilla random permutation. Null generation 
must therefore respect temporal and common-driver structure. Kernel or scale hyperparameters are 
chosen inside nested validation. Dependence alone supplies neither direction nor mechanism.
DEPENDENCE_TEST(X, Y, null_registry, family_id):
<PARSED TEXT FOR PAGE: 10 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 validate point-in-time alignment and ancestry
 choose HSIC configuration inside inner training fold
 compute observed statistic
 generate dependence-preserving null appropriate to time series
 compute empirical p
 register p in multiplicity family
 apply family correction
 if q survives and independent replication exists:
 advance status
 else:
 retain as exploratory/non-predictive
10. Sequential inference and regime detection
Bayesian Online Change Point Detection is the default sequential detector. Its prior parameter is named 
changepoint_rate_prior rather than hazard to avoid confusion with the downstream survival hazard. 
SPRT and CUSUM are alternatives for suitable observation models.
BOCPD_UPDATE(x_t):
 for each run length r:
 evaluate predictive probability p(x_t | run_length=r, sufficient_stats_r)
 growth_prob[r+1] = posterior_prev[r] * (1-cp_rate) * predictive
 cp_prob[0] += posterior_prev[r] * cp_rate * predictive
 normalise posterior
 update sufficient statistics
 emit posterior run-length distribution and change probability
Entry, maintenance, exit, minimum-run and cooldown thresholds constitute hysteresis. All thresholds 
are selected inside nested validation; they cannot be tuned on the outer holdout.
11. Stage A to Stage B predictive architecture
11.1 Stage A feature construction
Stage A removes algebraic identities before statistical selection. Sparse-group regularisation may be 
used to handle grouped dependence while preserving domain structure. Conceptual groups include 
G1=[drift,cascade,jump], G2=[recovery_loss,oscillatory_instability], 
G3=[fragmentation,crowding,propagation], and optional G23 coupling.
11.2 Stage B supervised transition model
PCA is not the default because unsupervised variance directions need not preserve outcome 
information. PLS-Cox is the default supervised projection/survival combination where proportional￾hazards assumptions are adequate. The projection is trained entirely within each training fold.
<PARSED TEXT FOR PAGE: 11 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
The earlier hand-written hazard h(t)=h0 exp{aG1+bσ+c dλ1/dt} is retired as a derivation. Stochastic and 
spectral machinery may engineer defensible features, but transition hazard must be calibrated 
statistically from frozen features.
TRAIN_STAGE_B(training_ledger):
 remove unavailable, unidentified and ancestry-duplicate features
 fit Stage-A transformations using training data only
 fit supervised projection (default PLS) inside inner CV
 fit survival/transition model on projected features
 test proportional-hazard and calibration assumptions
 compare against registered benchmark ladder
 freeze all transformations, coefficients and thresholds
 evaluate once on outer holdout
12. Sidecar architecture
Sidecars are domain-specific observation and feature systems feeding the common evidence ledger. 
They do not receive permission to bypass the constitutional rules. Current named sidecars include 
BADL/BADL-M for markets, GISC for geopolitical instability, CTSC for climate transition, TPSS for 
technological phase shift, CCSC for corporate collapse and SCFS for supply-chain fracture.
SIDECAR_INTERFACE:
 sidecar_id
 domain
 observation_contracts[]
 feature_contracts[]
 ancestry_edges[]
 null_models[]
 benchmark_models[]
 output:
 Signal # measured state, not narrative label
 Vector # multidimensional evidence representation
 Hazard # only if calibrated to an Outcome Contract
 forbidden:
 inferred_intent_without_evidence
 scalar_composite_without_identification
 hidden_revisions
 unregistered lag search
Conflicting sidecar models remain separate. They are not averaged merely to make disagreement 
disappear. A market outlier score of Cobb-Douglas form, for example O=(S^0.30 C^0.20 N^0.15 T^0.15 
A^0.20)/(R^0.60 F^0.40), is explicitly a modelling choice rather than a result derived from Itô calculus. It 
remains candidate machinery until validated against a defined outcome.
<PARSED TEXT FOR PAGE: 12 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
13. Historical anchors, motifs and cyclic history
13.1 What 'cycle' means
The framework does not assume fixed-period historical cycles. It separately tests periodicity, quasi￾cycles, state recurrence, sequence recurrence, structural recurrence and memetic recurrence. Cycles 
are paths through state space, not numerology.
The core search is X_{t w:t} X_{j w:j}, followed by a predictive test of P(X_{t+h}|X_{t w:t}) against − ≈ − −
unconditional and simple models. A phase variable φ_t [0,2π) is used only where empirically ∈
identifiable.
13.2 Temporal hierarchy
The hierarchy is Event Anchor Motif Cycle Cycle family. The objective is to predict the next → → → →
transition conditional on the present trajectory, not to assert that history repeats.
13.3 Anchor representation
A full anchor may be written A_t=(X_t, Xdot_t, T_t, φ_t, U_t), or operationally as levels, directions, 
response elasticities, persistence and topology. Historical similarity is multidimensional; 
D_A=(D_S,D_X,D_R,D_E) should not be collapsed until weights are validated.
Anchor classes are R recurrence, T transition, F false-positive, N normalisation/recovery, D divergence 
and C counter-anchor. Divergence anchors satisfy low pre-outcome distance but high post-outcome 
distance and are essential for learning cycle-breakers.
13.4 Shock geometry and transmission response
Shock Geometry is SG_t=[Δx/σ_Δx, speed, persistence, breadth, cross-asset response]. An anchor may be 
decomposed as A_t=(SG_t,TR_t), separating source geometry from propagation response. Same shock 
does not imply same propagation network.
13.5 Anchor uncertainty
U_A=[U_measurement,U_source,U_reconstruction,U_distance,U_outcome,U_sampling]. Historical 
similarity without these uncertainty components is not production evidence.
ANCHOR_RETRIEVAL(current_trajectory, historical_store, frozen_metric):
 exclude any historical information dated after each candidate anchor's forecast origin
 reconstruct candidate features from historical vintages where available
 calculate multidimensional state and trajectory distances
 propagate anchor uncertainty into distance uncertainty
 retrieve nearest recurrence, divergence, false-positive and normalisation anchors
 forecast outcome using frozen neighbour rule
 compare with base rate, persistence and conventional kNN
 if Psychohistory representation does not improve outer loss:
 do not admit anchor complexity
13.6 Hierarchical atlases
Candidate atlases include A^M memetic, A^F financial, A^P participation, A^I institutional, A^E 
economic, A^L network and other domain atlases. Composite A* = A^M A^P A^E A^I A^L is not ⊕ ⊕ ⊕ ⊕
<PARSED TEXT FOR PAGE: 13 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
a scalar average; the direct-sum notation preserves domain structure until a validated supervised 
combination exists.
14. Propagation graphs
The Exposure Propagation Graph G_X(t)={V_X,E_X,W_X} represents pathways by which an exposure 
may spread. The Response Propagation Graph G_R(t)={V_R,E_R,W_R} represents observed responses. 
Exposure breadth is not response breadth.
Candidate conversion C_XR(t,h)=P(R_{t:t+h}|X_t) is not admitted until exposure, response and horizon 
definitions are frozen.
EDGE_LOCAL_VALIDATION(edge A_to_B):
 freeze A, B, lag/horizon, confounder set, null and outcome vintage
 verify temporal availability and ancestry
 fit simple A-only benchmark and declared conditional alternatives
 test predictive increment on untouched data
 correct within registered edge family
 require replication where feasible
 never infer B_to_C from A_to_B result
15. Outcome contracts and prospective forecast ledger
15.1 Outcome Contract
OutcomeContract:
 event_id
 domain
 observable_definition
 threshold_or_rule
 forecast_horizon
 event_start_rule
 event_end_rule
 minimum_separation
 ambiguous_case_policy
 authoritative_source
 point_in_time_availability_rule
 revision_policy
 target_vintage:
 first_release | settled_vintage | explicit_revision_target
 scoring_rule
 expiry_rule
<PARSED TEXT FOR PAGE: 14 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
No defined event and horizon means no forecast score. Repeated forecasts concerning one underlying 
event are dependent; individual Brier scores may be recorded, but inference, false-alert rates and 
replication statistics must cluster by outcome episode or use non-overlapping windows.
15.2 Forecast ledger
ForecastRecord:
 forecast_id
 issued_at
 information_cutoff
 model_version_hash
 outcome_contract_id
 probability
 forecast_class_if_any
 horizon
 expiry_time
 component_vintages[]
 feature_values[]
 baseline_predictions[]
 unresolved_at_issue = true
 later:
 resolved_outcome
 outcome_vintage
 resolution_time
 brier
 log_score
 calibration_bin
 lead_time_definition
15.3 Brier score
For a binary event y_i {0,1} and forecast probability p_i, BS=(1/N)Σ(p_i y_i)^2. A model's Brier score is ∈ −
reported only for prospectively frozen forecasts whose outcomes have matured under the same 
contract. Skill may be expressed relative to a baseline as BSS=1 BS_model/BS_baseline when the −
denominator is appropriate and non-zero.
15.4 Calibration
Calibration is assessed using reliability curves and, once sample size supports it, calibration intercept 
and slope. Sparse event counts require uncertainty intervals and discourage overinterpretation. 
Calibration cannot be estimated meaningfully from a handful of hand-selected forecasts.
15.5 Lead time and false alerts
Lead time is measured from the first valid, frozen warning satisfying its persistence rule to the event 
start defined by the Outcome Contract. A warning that merely republishes a recognised leading 
<PARSED TEXT FOR PAGE: 15 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
indicator does not earn incremental lead. False alerts require forecast expiry; an unresolved warning is 
not yet false.
16. Validation constitution
16.1 Data partitions
D_development is inspectable and may be used to design the system. D_validation is used for pre￾specified model selection under controlled access. D_lockbox remains untouched until a frozen periodic 
evaluation. Any period inspected during architecture development becomes DEVELOPMENT-EXPOSED. 
October 2026 is therefore development-exposed.
16.2 Benchmark ladder
Every domain begins with the simplest defensible comparator. The generic ladder is Base rate simple →
statistical/persistence model recognised leading indicator minimal multivariate baseline single G → → →
family G1+G2+G3 sidecars interactions. Additional structure survives only if it improves → → →
untouched predictive loss.
16.3 Information-inheritance baseline
If Psychohistory consumes an external forecast, expectation series or recognised leading indicator, it 
must outperform that input itself. Skill(PH) Skill(external forecast)>0 is the relevant incremental test, −
not merely PH versus a naïve base rate.
16.4 Ablation
For component j, ΔS_j=S(M+j) S(M), where S is a proper held-out scoring metric and M is the simpler −
model. Components that fail to improve held-out performance are demoted or removed even if their 
narrative interpretation is appealing.
16.5 Embargo
Temporal cross-validation uses an embargo E at least as long as the maximum effective lookback of all 
features, including nested smoothing and inherited parent estimators. This prevents adjacent training 
observations from leaking information into the test window.
17. Complete evaluation algorithm
PSYCHOHISTORY_2_4_EVALUATION_CYCLE(cutoff_time):
 1. FREEZE INFORMATION
 set information_cutoff = cutoff_time
 ingest only records with availability_time <= cutoff_time
 preserve exact vintages and source versions
 2. UPDATE PROVENANCE
 build/update Evidence Ancestry Graph
<PARSED TEXT FOR PAGE: 16 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 mark nested geography, shared survey systems, transforms and revisions
 calculate observed breadth; do not invent informational breadth if unidentified
 3. VALIDATE OBSERVATIONS
 check units, scale semantics, reference horizon, publication horizon
 check composition stability and information maturity
 route defective observations to exclusion or uncertainty penalty
 4. UPDATE G1
 dispatch narrative processes
 fit only preregistered candidate families
 update source-tree/genealogy hypotheses
 keep descendants ancestry-linked
 5. UPDATE G2
 fit local stability models where observation model supports them
 compute diagnostic residuals with uncertainty
 route departure to transition / alternative process / generic misfit
 6. UPDATE G3
 build operator-specific network vintages
 estimate Laplacian, covariance and exposure diagnostics separately
 attach spectral resolution and perturbation uncertainty
 7. TEST G23 ONLY WHERE CONTRACT PASSES
 enforce identifiability, lag registration and embargo
 evaluate incremental predictive loss
 test registered surrogate null
 unresolved null => TEST_UNRESOLVED
 8. UPDATE SIDECARS
 construct domain vectors without unsupported scalar collapse
 separate shock from exposure, state from hazard, current from pipeline
 retain competing models rather than averaging disagreement
 9. UPDATE HISTORICAL ANCHORS
 use pre-outcome historical information only
 retrieve recurrence and counter-anchors under frozen metric
<PARSED TEXT FOR PAGE: 17 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 propagate reconstruction uncertainty
 compare with conventional kNN
 10. UPDATE HYPOTHESIS REGISTRY
 add newly declared tests before inspecting their outcomes
 apply multiplicity correction within frozen families
 do not promote exploratory relations without replication
 11. GENERATE FORECASTS
 for every active Outcome Contract:
 compute baseline forecasts
 compute Psychohistory forecast using frozen model version
 store complete ForecastRecord before outcome observation
 assign expiry/resolution rule
 12. RESOLVE MATURE OUTCOMES
 use declared authoritative source and target vintage
 cluster repeated forecasts by outcome episode
 compute proper scores only for resolved frozen forecasts
 13. SCORE
 Brier, log score, calibration diagnostics, false-alert rate,
 lead time, discrimination metrics as sample size permits
 compare every metric with corresponding baseline
 report uncertainty
 14. ABLATE
 test incremental value of G1, G2, G3, sidecars and interactions
 demote components with no held-out improvement
 15. AUDIT FAILURE MODES
 search for leakage, overfitting, redundancy, weak identification,
 invalid nulls, composition shifts, ancestry duplication,
 horizon aliasing and unsupported causal/intent claims
 16. SPECIFICATION CHANGE GATE
 change specification only if:
 evidence identifies a concrete failure
<PARSED TEXT FOR PAGE: 18 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 change is minimal
 change can be frozen prospectively
 held-out improvement can be assessed
 otherwise preserve current specification
 17. REPORT
 evidence observed
 failures found
 changes made and reason
 scoring status
 unresolved hypotheses
 next prospective tests
18. Composition, substitution and aggregation
Aggregate change may be decomposed conceptually as WithinGroupChange + CompositionChange. 
Where categories compete for the same activity, add SubstitutionEffect. A rise in one technology and fall
in another may reflect substitution rather than two independent demand signals.
Composition stability is required before interpreting an aggregate as a stable state variable. For 
example, payment failures across heterogeneous categories cannot be treated as a single household￾stress mechanism if the category mix changes materially.
AGGREGATE_AUDIT(groups_t, groups_prev):
 align group definitions and weights
 estimate within-group change
 estimate change attributable to weight/composition shifts
 identify mutually substitutable categories
 if decomposition is not identifiable:
 flag aggregate as mechanism-heterogeneous
 prohibit causal scalar interpretation
19. Revision robustness and information maturity
Candidate features from revisable sources are tested for state robustness, direction robustness and 
magnitude robustness across vintages. A feature that looks predictive only in final revised history is not 
a valid real-time predictor.
REVISION_ROBUSTNESS(feature_id, vintage_store):
 reconstruct feature at each historical publication vintage
 compare:
 categorical/state classification
 direction/sign
 magnitude/rank
<PARSED TEXT FOR PAGE: 19 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 quantify instability without using future outcome for threshold selection
 if real-time instability is material:
 downgrade or exclude feature
The latest ONS quarterly-national-accounts documentation available at this storage date reports a mean 
absolute revision of 0.24 percentage points between the first estimate and the later quarterly estimate. 
Earlier ONS releases have reported different figures, including 0.28 percentage points for first estimate 
versus the same quarter three years later. Revision magnitude is therefore stored as versioned 
empirical metadata, never a universal constant.
20. State, hazard and transmission
Current observed state S_t and future transition hazard H_{t,h}=P(future adverse transition|I_t) are 
separate. An economy may already be weak without having high probability of a new deterioration; 
conversely, a currently benign state may carry elevated transition risk.
Transmission is neither instantaneous nor monotonic. Hedging, inventories, savings, fixed-price 
contracts, fiscal intervention, spare capacity and substitution can suppress, delay or redirect 
propagation. Therefore an upstream shock is not proof of downstream outcome.
20.1 Energy-inflation example as an unresolved prospective fork
The current development evidence illustrates the rule. The September 2026 Bank of England record 
states that higher energy prices increased the near-term inflation outlook while indirect pass-through 
through firms' supply chains had been small to date and less than expected at the start of the conflict. 
MPC members disagreed over the likelihood of meaningful second-round effects. Psychohistory 
therefore stores competing hypotheses rather than declaring the wage/expectations edge validated.
ENERGY_FORK:
 E0 = upstream energy prices
 E1 = direct household/firm energy exposure
 E2 = firm input costs
 E3 = output prices
 E4 = headline CPI
 E5 = inflation expectations
 E6 = wage setting
 E7 = persistent underlying inflation
For each edge E_i -> E_{i+1}:
 define measurement contract
 define lag/horizon before outcome
 define buffers/common drivers
 validate edge locally
 preserve unresolved status until evidence matures
<PARSED TEXT FOR PAGE: 20 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
21. Historical memetic case: Reformation test bed
The Reformation is retained as a methodological test case rather than proof of the model. Wittenberg in 
1517 is an approximate origin point for a rapidly propagating reform complex; printing presses can be 
represented as high-reproduction carrier nodes, while universities, churches and trade routes 
contribute network structure. The traditional door-nailing story is not treated as a hard observation 
because its historicity is contested. The firmer modelling target is the circulation and mutation of texts 
and arguments.
Institutional opposition may amplify exposure, but this is a candidate mechanism requiring historical 
evidence rather than an assumed paradoxical effect. Source-tree inference must permit secondary hubs 
and multiple ignition points. Archival survivorship and uneven recording are explicit observation￾process uncertainties.
22. Failure catalogue
Failure Why it matters Required response
Future leakage inflates apparent skill reconstruct point-in-time 
vintages; embargo
Transform duplication multiplies one signal ancestry-link transforms; ablate
Nested geography false replication multiplicity/ancestry link
Expert pseudo-replication interpretation repeats 
underlying data
retain interpretive ancestry
Horizon aliasing current/pipeline/future 
collapsed
store horizon semantics
Publication lead illusion fast release mistaken for 
predictive lead
compare phenomenon horizon
Shock=exposure homogeneous impact assumed model exposure/buffers 
separately
State=hazard bad present mistaken for future
transition
separate S_t and H_t,h
Edge chaining one validated edge licenses 
whole story
edge-local validation
Invalid surrogate null false significance TEST_UNRESOLVED
Post-hoc lag search min-p fishing register lags; nested selection
Final-vintage backtest uses future revisions vintage reconstruction
Composition drift aggregate meaning changes decompose or downgrade
Substitution misread category shifts counted as 
multiple forces
model substitution
Intent attribution patterns treated as motive neutral coordinated_activity 
label
<PARSED TEXT FOR PAGE: 21 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
Scalar collapse heterogeneous vector reduced 
prematurely
retain vector until validated
Historical determinism similarity treated as destiny counter-anchors + OOS 
comparison
23. Reference implementation schema
23.1 Directory structure
psychohistory/
 config/
 outcome_contracts/
 hypothesis_registry/
 surrogate_registry/
 sidecars/
 data/
 raw_vintages/
 observation_records/
 historical_anchors/
 forecast_ledger/
 core/
 provenance.py
 vintages.py
 measurement.py
 multiplicity.py
 scoring.py
 validation.py
 g1/
 process_dispatch.py
 hawkes.py
 jumps.py
 source_tree.py
 genealogy.py
 g2/
 ou.py
 diagnostics.py
 transition_signatures.py
 g3/
 laplacian.py
<PARSED TEXT FOR PAGE: 22 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 covariance.py
 exposure.py
 spectral_uncertainty.py
 g23/
 coupling.py
 surrogates.py
 anchors/
 representation.py
 retrieval.py
 counteranchors.py
 sequential/
 bocpd.py
 cusum.py
 sprt.py
 models/
 stage_a.py
 pls_cox.py
 baselines.py
 calibration.py
 reports/
 evaluation_cycle.py
 audit.py
23.2 Deterministic model versioning
MODEL_VERSION_HASH =
 hash(
 source_code_commit,
 outcome_contract_versions,
 feature_contract_versions,
 hypothesis_registry_snapshot,
 sidecar_config,
 training_data_vintage_manifest,
 random_seed_manifest
 )
Every forecast stores the version hash. Re-running a historical forecast with a different hash creates a 
new development experiment, not a replacement for the original forecast.
<PARSED TEXT FOR PAGE: 23 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
24. Baseline specifications
24.1 Generic binary transition baseline
B0: empirical base rate estimated on training period only
B1: persistence/current-state model
B2: seasonal or autoregressive conventional model
B3: recognised leading indicator alone, if consumed by PH
B4: minimal multivariate conventional model
PH: frozen Psychohistory model
24.2 Housing example
The housing ladder is B0 price persistence; B1 mortgage approvals; B2 approvals plus rates; PH adds 
only predeclared network, exposure or sidecar structure. Mortgage approvals are already a recognised 
leading indicator, so a Psychohistory model that merely reproduces them has no demonstrated 
incremental value.
24.3 PMI/GDP example
The GDP ladder is persistence PMI regime raw PMI or conventional PMI mapping Psychohistory. → → →
First-release GDP is the primary real-time target unless a different target vintage is frozen prospectively.
Mature GDP may be a secondary latent-state target, but it cannot silently replace the first-release target 
after outcomes are known.
25. Current empirical status as of 6 October 2026
The framework remains in development. October 2026 observations have been inspected and are 
therefore development-exposed. No current observation may be retrospectively promoted into a 
successful forecast if a frozen probability did not exist before its outcome.
The current UK macroeconomic evidence is heterogeneous rather than a single latent stress state. Bank 
of England September material records a higher near-term inflation outlook due to energy while stating
that indirect supply-chain pass-through had been small so far; the MPC was split 6–3 between holding 
Bank Rate at 3.75% and raising it to 4%. This is development evidence for competing transmission 
hypotheses, not a validated Psychohistory forecast.
ONS national-accounts releases demonstrate that GDP is revisable and that revision properties 
themselves change with the comparison vintage and period. This directly supports the Outcome Vintage
Declaration and Revision Robustness requirements.
Metric Current legitimate status
Aggregate Psychohistory Brier score Not yet available
Calibration slope/intercept Not yet available
False-alert rate Not yet available
Demonstrated incremental lead time Not yet available
Validated G23 coupling None promoted
<PARSED TEXT FOR PAGE: 24 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
Validated scalar economic-stress composite None promoted
Prospective lockbox performance Not yet matured
October 2026 data Development-exposed
26. Domains scheduled for disciplined expansion
Future domain work may include infectious-disease outbreaks and commercial activity, banking and 
lending, property transactions and prices, gold purchasing, pensions, cultural/arts expansion and 
contraction, and violence or hostility directed at disabled people. Each requires a separate 
measurement contract and cannot be imported merely because it sounds historically relevant.
For infectious disease, laboratory-confirmed incidence, syndromic surveillance, testing policy, 
healthcare utilisation, commercial mobility and spending are different observation processes. 
Commercial data may provide timeliness but must not be mistaken for incidence. For disability-related 
attacks, recorded hate crime, victimisation surveys, reporting propensity, police practice and media 
volume must remain distinct; news volume is not incidence and intent cannot be inferred from 
aggregate pattern alone.
27. Falsification programme
Psychohistory 2.4 should be abandoned or materially simplified if its additional structure repeatedly 
fails to improve proper held-out scores over conventional baselines. The framework is not protected by 
interpretability, historical richness or narrative plausibility.
 Reject a component if repeated preregistered ablations show no incremental held-out value.
 Reject a coupling if its null is invalid, parameters are weakly identified, or predictive increment 
does not replicate.
 Reject a historical motif if conventional k-nearest-neighbour recurrence performs as well or better.
 Reject a sidecar scalar if its component vector performs better or if the scalar changes meaning 
under composition shifts.
 Reject claimed lead time if the advantage disappears after comparison with the recognised leading 
indicator supplying the information.
 Reject causal language where only predictive dependence has been established.
 Prefer a smaller model when performance is statistically indistinguishable within uncertainty.
28. Reproducible research protocol
FOR EACH REGISTERED EXPERIMENT:
A. Before outcome access:
 freeze question
 freeze outcome contract
 freeze source/vintage rules
 freeze candidate models
<PARSED TEXT FOR PAGE: 25 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 freeze lags/horizons
 freeze multiplicity family
 freeze scoring metrics
 freeze exclusion rules
B. During development:
 use D_development only
 nested-select hyperparameters
 maintain complete hypothesis ledger
 record failed experiments
C. Validation:
 evaluate on D_validation under embargo
 permit only predeclared decision rule for promotion
D. Lockbox:
 freeze final model
 evaluate once
 store all predictions and baselines
 do not tune from lockbox errors
E. Reporting:
 report all registered models
 report uncertainty and missing outcomes
 cluster outcome episodes
 disclose revisions and source defects
 distinguish exploratory, replicated and admitted evidence
29. Minimal production pseudocode
def forecast_cycle(cutoff):
 obs = ingest_point_in_time(cutoff)
 obs = measurement_audit(obs)
 ancestry = build_evidence_ancestry(obs)
 g1 = run_g1(obs, ancestry)
 g2 = run_g2(obs, ancestry)
 g3 = run_g3(obs, ancestry)
 g23 = run_g23_if_identifiable(g2, g3, obs)
<PARSED TEXT FOR PAGE: 26 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 sidecars = run_sidecars(obs, ancestry)
 anchors = retrieve_historical_anchors(
 current=(g1, g2, g3, sidecars),
 point_in_time=True,
 include_counteranchors=True
 )
 features = assemble_features(
 g1, g2, g3, g23, sidecars, anchors,
 remove_algebraic_duplicates=True,
 preserve_vectors=True
 )
 for contract in active_outcome_contracts(cutoff):
 baselines = predict_registered_baselines(contract, obs)
 ph_prob = predict_frozen_ph_model(contract, features)
 write_forecast_record(
 cutoff=cutoff,
 contract=contract,
 probability=ph_prob,
 baselines=baselines,
 vintages=manifest(obs)
 )
 resolve_only_mature_outcomes(cutoff)
 score_only_frozen_forecasts()
 run_failure_audit()
30. What is deliberately not specified
Several quantities remain deliberately unspecified because the evidence does not yet justify universal 
choices. These include a universal weighting of M/P/E/I/L, a universal informational-breadth estimator, 
a fixed anchor-distance weighting, a universal memetic reproduction number, a scalar national 
economic-stress index, a universal coupling lag, and fixed thresholds for sequential warning states. 
These must be estimated within declared domains and validated prospectively or remain absent.
Likewise, stochastic calculus does not derive the transition hazard. Black-Scholes and GBM are retained 
only as counter-models or feature-engineering tools where economically appropriate. The survival 
model is a statistical calibration layer.
<PARSED TEXT FOR PAGE: 27 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
31. Discussion
The principal contribution of Psychohistory 2.4 is not a claim that history can be forecast by discovering
a hidden deterministic cycle. It is an attempt to make a much weaker proposition testable: systems can 
revisit partially similar configurations, and the combination of state, trajectory, topology, propagation 
and response may sometimes contain information about the next transition. The framework earns the 
name only if that information survives point-in-time reconstruction, multiplicity correction, simple 
baselines and prospective scoring.
The architecture has become more conservative as it has developed. Several apparently useful scalar 
constructs have been refused because they were underidentified. Network edges are no longer allowed 
to inherit validity from neighbouring edges. Current state, momentum, pipeline and expectations are 
separated. Transform ancestry prevents four versions of one series from becoming four votes. 
Historical anchors include counterexamples. Expert judgement is useful but retains ancestry to the 
observations from which it was formed. These restrictions reduce the number of dramatic conclusions 
the model can make, which is desirable if they reduce false confidence.
The remaining scientific risk is complexity itself. A sufficiently elaborate framework can explain almost 
anything after the fact. Psychohistory 2.4 therefore succeeds only if its additional structure improves 
untouched predictive performance. If persistence, a recognised leading indicator or a conventional 
multivariate model performs equally well, the more complicated machinery should be removed. The 
prospective ledger, rather than the elegance of the architecture, is the final judge.
32. Conclusion
Psychohistory 2.4 is now specified as a leakage-resistant forecasting research programme rather than a 
narrative forecasting system. Its state representation, memetic machinery, local-stability diagnostics, 
operator-specific network analysis, optional coupling layer, historical-anchor retrieval, sidecars and 
supervised hazard calibration are subordinate to three rules: measure what is actually observed, do not 
multiply dependent evidence, and do not infer a network story from local significance.
The immediate research objective is prospective validation. Frozen outcome contracts, exact vintages, 
baseline forecasts and expiry rules must accumulate before aggregate Brier skill, calibration, false-alert 
performance or lead-time advantage can be claimed. Until that evidence exists, the correct empirical 
conclusion is not that Psychohistory works or fails, but that the architecture is sufficiently specified to 
be tested without silently moving the goalposts.
Appendix A. Mathematical reference
 dX = μ(X,t)dt + σ(X,t)dB.
 OU: dX = aXdt + σdB; stationary variance σ²/(2a); lag correlation exp( aΔ); recovery time 1/a. − −
 Hawkes: λ(t)=μ+Σ α exp[ β(t t_i)]; branching ratio n=α/β. − −
 Simple contagion: P(adopt|k)=1 (1 p)^k. − −
 Exposure kernel: K_M(i,j,Δt)=P(j receives/adopts M | i,Δt,C,L,I).
 Coupling: xdot_i=f(x_i)+κΣ_j L_ijH(x_j).
 Modal coupling: ηdot_k=[Df(s)+κγ_kDH(s)]η_k.
 Fiedler rotation: 1 |<v_t,v_{t Δ}>|. − −
 Empirical surrogate p=(1+Σ1(ΔL_null ΔL_obs))/(B+1). ≥
<PARSED TEXT FOR PAGE: 28 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
 Future hazard: H_{t,h}=P(event in horizon h | information available at t).
 Brier score: BS=(1/N)Σ(p_i y_i)². −
 Brier skill: BSS=1 BS_model/BS_baseline. −
 Anchor divergence: D_pre << 1 and D_post >> 1.
 Shock geometry: SG=[standardised magnitude,speed,persistence,breadth,cross-asset response].
Appendix B. Storage-status registry
Item Status Reason
G1 process dispatch Specified requires domain-specific 
validation
G1 source-tree inference Specified/candidate posterior model requires data￾specific likelihood
R_M* Concept only no identifiable universal 
estimator
G2 OU diagnostics Specified valid only where local OU 
model adequate
G3-L/C/A Specified operator-specific validation 
required
G23 coupling Conditional production only after contract 
passes
HSIC/dCov dependence Specified requires serial-dependence￾aware null
BOCPD Default candidate thresholds nested-validated
PLS-Cox Stage B Default candidate must beat simpler survival 
models
Historical anchor engine Specified/candidate must beat conventional kNN
BADL/GISC/CTSC/TPSS/CCSC/
SCFS
Interfaces specified domain estimators not 
universally validated
Aggregate predictive skill Unmeasured prospective ledger insufficient
Appendix C. Source notes for the storage edition
The framework itself is a research specification. The following current-source notes are included only to
document empirical claims used in the 6 October 2026 development audit; they are not presented as 
validation results.
Source Use in this paper
Bank of England, Monetary Policy Summary and 
Minutes, September 2026
Bank Rate held at 3.75% by 6–3; three members 
preferred 4%. The release states that direct 
energy effects increased the near-term inflation 
outlook while indirect supply-chain pass-through 
<PARSED TEXT FOR PAGE: 29 / 29>
Psychohistory 2.4 — storage edition — 6 October 2026
had been small to date and less than expected.
Bank of England, Clare Lombardelli speech, 24 
September 2026
Discusses the size and volatility of the energy 
shock, economic response and underlying 
inflation dynamics; supports treating 
transmission as uncertain and sequential.
Office for National Statistics, GDP quarterly 
national accounts, April–June 2026
Q2 2026 GDP estimated at 0.5%, revised up 0.1 
percentage points; latest release reports a 0.24 
percentage-point mean absolute revision 
between first and later quarterly estimates.
Office for National Statistics, GDP first quarterly 
estimate methodology/release material
Earlier releases report approximately 0.28 
percentage points between first estimate and the 
same quarterly estimate three years later, 
illustrating that revision metrics depend on 
comparison definition and vintage.
Office for National Statistics, National Accounts 
Revisions Policy, 2026
National accounts are integrated and revisions to 
one area can propagate through the system; 
supports explicit vintage and revision 
provenance.
Appendix D. Change log consolidated through 6 October 2026
 Replaced raw narrative acceleration with process dispatch for diffusion, jumps, Hawkes or null.
 Split G1 into dynamics, source-tree, genealogy/mutation and downstream influence.
 Removed G3-J because it duplicated G2 spectral-abscissa information.
 Made G3 operator-specific: Laplacian, covariance and exposure networks.
 Added diagnostic uncertainty and model-departure routing.
 Added G23 coupling contract, surrogate registry, embargo and edge-local validation.
 Added Evidence Ancestry Graph and informational-breadth constraint.
 Added hypothesis registry, FDR accounting and status ladder.
 Added Outcome Contracts, prospective Forecast Ledger and outcome-episode accounting.
 Added phenomenon lead versus publication lead.
 Added observation-process provenance and information maturity.
 Added composition stability, substitution awareness and transform ancestry.
 Added outcome-vintage declaration and revision-robustness testing.
 Added information-inheritance baselines for external forecasts and leading indicators.
 Added State-Hazard Separation.
 Added Shock-Exposure Separation.
 Added Horizon Semantics and State-Momentum Orthogonality.
 Added interpretive evidence ancestry for expert/institutional judgement.
 Formalised counter-anchors, divergence anchors, trajectory distance and anchor uncertainty.
 Locked October 2026 as development-exposed.
 Retained zero demonstrated aggregate OOS performance until prospective scoring matures.