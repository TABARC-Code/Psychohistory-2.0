# Psychohistory 2.4 — Complete Mathematical & Algorithmic Specification

> Recovered text export of the canonical 2026-10-06 DOCX held in the ChatGPT project Library. The source DOCX SHA-256 is `bd1e29c516f46e053330c847b2d6fb81d4778de0b5e0da92330e9d2a38570ddb`; canonical PDF SHA-256 is `13c9af1972934faf78e6c276cb85414f3fc76d87dc8ca0fccfa6d403b0689ae5`. This UTF-8 export is provided so the full specification is inspectable in GitHub; the binary originals remain canonical.

<PARSED TEXT FOR PAGE: 1 / 74>
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
<PARSED TEXT FOR PAGE: 2 / 74>
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
<PARSED TEXT FOR PAGE: 3 / 74>
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
<PARSED TEXT FOR PAGE: 4 / 74>
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
<PARSED TEXT FOR PAGE: 5 / 74>
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
<PARSED TEXT FOR PAGE: 6 / 74>
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
<PARSED TEXT FOR PAGE: 7 / 74>
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
<PARSED TEXT FOR PAGE: 8 / 74>
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
<PARSED TEXT FOR PAGE: 9 / 74>
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
<PARSED TEXT FOR PAGE: 10 / 74>
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
<PARSED TEXT FOR PAGE: 11 / 74>
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
<PARSED TEXT FOR PAGE: 12 / 74>
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
<PARSED TEXT FOR PAGE: 13 / 74>
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
<PARSED TEXT FOR PAGE: 14 / 74>
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
<PARSED TEXT FOR PAGE: 15 / 74>
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
<PARSED TEXT FOR PAGE: 16 / 74>
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
<PARSED TEXT FOR PAGE: 17 / 74>
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
<PARSED TEXT FOR PAGE: 18 / 74>
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
<PARSED TEXT FOR PAGE: 19 / 74>
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
<PARSED TEXT FOR PAGE: 20 / 74>
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
<PARSED TEXT FOR PAGE: 21 / 74>
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
<PARSED TEXT FOR PAGE: 22 / 74>
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
<PARSED TEXT FOR PAGE: 23 / 74>
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
<PARSED TEXT FOR PAGE: 24 / 74>
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
<PARSED TEXT FOR PAGE: 25 / 74>
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
<PARSED TEXT FOR PAGE: 26 / 74>
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
<PARSED TEXT FOR PAGE: 27 / 74>
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
<PARSED TEXT FOR PAGE: 28 / 74>
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
<PARSED TEXT FOR PAGE: 29 / 74>
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
<PARSED TEXT FOR PAGE: 30 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
Part II — Complete Mathematical and Algorithmic Specification
Normative expansion. Part I is retained as the architectural synopsis. Part II supplies the estimator-level
definitions, likelihoods, optimisation rules, uncertainty procedures, failure states, validation gates and 
end-to-end algorithms required to implement Psychohistory 2.4 without relying on undocumented 
conversational context.
Status convention: SPECIFIED means the mathematical/algorithmic contract is defined; CANDIDATE 
means the machinery may be implemented but has not earned predictive admission; ADMITTED 
requires prospective held-out evidence; UNRESOLVED means identifiability, null validity or evidence is 
insufficient. No equation in this part is itself evidence of predictive skill.
33. Notation, probability space and time semantics
All stochastic quantities are defined on a filtered probability space (Ω,F,{F_t},P). F_t denotes the 
information genuinely available by forecast origin t, not a retrospectively reconstructed information 
set. Every production forecast must be F_t-measurable. If a quantity requires a revision, publication or 
reconstruction that arrived after t, it is not in F_t and cannot be used in the forecast.
Forecast admissibility: Z_t is admissible ⇔ Z_t is F_t-measurable under the stored vintage 
manifest.
Calendar time, event time, publication time and effective/reference time are distinct. Let r_i be the 
reference interval of observation i, p_i its publication time, a_i its actual availability time to the system, 
and h_i any semantic forecast horizon embedded in the observation. The ingestion layer stores all four. 
Availability, rather than reference date, controls leakage.
D_t^(v) = {o_i : a_i ≤ t, source_version_i = v_i(t)}.
For irregularly sampled processes, Δ_i=t_i t_{i 1} is retained explicitly. No estimator may silently treat − −
irregular observations as equally spaced. Aggregation onto a grid is a transform with its own ancestry 
and must record the aggregation kernel.
Symbol Definition
X_t canonical multidomain state [M,P,E,I,L], usually 
vector-valued
Y_{t,h} Outcome-Contract event in horizon h
F_t point-in-time information sigma-field
O_t validated observation set
T_E Evidence Ancestry Graph
G_X,G_R exposure and response propagation graphs
A_t historical anchor representation
Z_t admitted predictor vector
H_{t,h} calibrated future transition probability/hazard 
object
U uncertainty object; never assumed scalar unless 
justified
<PARSED TEXT FOR PAGE: 31 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
34. Measurement model
34.1 General observation equation
Every measured series is treated as an observation of a latent or operational quantity through an 
explicit observation operator. The general form is O_i = g_i(X_{r_i}, C_i, Q_i) + ε_i, where C_i contains 
composition and contextual variables, Q_i contains observation-process state, and ε_i is measurement 
error. The function g_i may be identity for directly operational quantities, but that identity must be 
declared rather than assumed.
O_i = g_i(X_{r_i}, C_i, Q_i) + ε_i, ε_i ~ E_i(θ_i).
Administrative counts, surveys, commercial transactions and media observations require different g_i. 
A police-recorded incident series, for example, is a function of underlying incidence, reporting 
propensity, recording policy, legal definition and classification practice. A payment-value series is a 
function of price, quantity, timing and contract structure. The framework therefore prohibits 
interpreting the observed number as the latent target unless the observation operator supports that 
interpretation.
34.2 Measurement-quality object
MEASUREMENT_QUALITY(o):
 verify source identity and publication timestamp
 verify units and scale semantics
 identify reference interval and horizon semantics
 identify revision state and information maturity
 identify sampling/composition frame
 attach known defects and methodological breaks
 estimate/attach measurement uncertainty where defensible
 set identifiable = TRUE/FALSE/PARTIAL
 if critical fields missing:
 route to EXPLORATORY_ONLY or EXCLUDE
34.3 Composition decomposition
ΔAggregate_t = WithinGroup_t + Composition_t + Substitution_t + Residual_t.
The decomposition is exact only when the aggregation rule and weights are known. Otherwise it is a 
conceptual accounting identity and the residual absorbs unobserved weighting and interaction effects. 
The system must not manufacture group-level contributions from an aggregate-only source.
35. Vintage store, revisions and real-time reconstruction
A real-time database stores every observed vintage rather than overwriting earlier releases. For 
variable j and reference time s, x_{j,s}^{(v)} denotes the value in vintage v. The forecast-time value is 
x_{j,s}^{(v(t))}, where v(t) is the latest vintage actually available at t.
x^RT_{j,s|t} = x_{j,s}^{( max{v : availability(v)≤t} )}.
Revision error for a later comparison vintage v* is R_{j,s}^{v*,t}=x_{j,s}^{(v*)} x_{j,s}^{RT|t}. Revision −
diagnostics are descriptive unless the revision itself is a registered target.
RECONSTRUCT_REAL_TIME_PANEL(cutoff):
 for each variable and reference period:
 select latest vintage with availability_time <= cutoff
 preserve missing values that were missing at cutoff
<PARSED TEXT FOR PAGE: 32 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 preserve historical methodology in force at cutoff
 prohibit backfill from later vintages
 return panel, vintage_manifest
Revision robustness has three axes: state robustness asks whether categorical interpretation changes; 
direction robustness asks whether sign/trend changes; magnitude robustness asks whether ranking or 
economically relevant size changes. A predictor that survives only in final-vintage history is demoted 
for real-time use.
36. Transform ancestry and algebraic-dependence elimination
Before model fitting, features are classified as free parameters, independent observables, derived 
quantities, diagnostic residuals or uncertainty measures. Algebraically determined quantities are 
removed from the independent-evidence count.
If z_k = f(z_1,…,z_m) deterministically, then rank_evidence({z_1,…,z_m,z_k}) ≤ 
rank_evidence({z_1,…,z_m}).
REDUNDANCY_GATE(features, ancestry):
 build deterministic-dependence map from transform definitions
 mark MoM/YoY/z-score/deviation variants sharing one parent
 mark OU-derived variance, recovery and autocorrelation expectations
 mark Hawkes n = alpha/beta as derived
 calculate candidate design-matrix rank inside training fold
 retain alternative transforms only as competing representations
 never count them as independent confirmations
Statistical collinearity is handled separately from algebraic dependence. The former can be regularised 
or selected; the latter is a bookkeeping fact and cannot be cured by regularisation.
37. G1-D: diffusion, drift and jump-process estimation
37.1 Continuous diffusion benchmark
For a scalar locally diffusive narrative statistic X_t, the generic Itô diffusion is 
dX_t=μ(X_t,t;θ_μ)dt+σ(X_t,t;θ_σ)dB_t. For small irregular intervals Δ_i, a quasi-likelihood approximation 
uses increments ΔX_i approximately Normal(μ_iΔ_i, σ_i²Δ_i). This approximation is permitted only when
sampling is sufficiently fine relative to process dynamics and jump diagnostics do not reject it.
ℓ(θ)=−1/2 Σ_i [ log(2πσ_i Δ_i) + (ΔX_i−μ_iΔ_i) /(σ_i Δ_i) ]. ² ² ²
Optimisation is constrained to parameter regions where σ_i>0. Standard errors use observed 
information only when regularity is credible; otherwise block/bootstrap procedures preserve serial 
structure.
37.2 Jump-diffusion
dX_t = μ_t dt + σ_t dB_t + J_t dN_t.
J_t is jump size and N_t a counting process. The production objective is not to fit a universal jump model 
but to prevent jumps from being mislabelled as continuous acceleration. Realised variance RV=Σr_i² 
may be decomposed with a jump-robust continuous-variation estimator such as bipower variation 
when sampling assumptions are defensible.
BV = (π/2) Σ_{i=2}^n |r_i||r_{i−1}| (regular-grid reference form).
<PARSED TEXT FOR PAGE: 33 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
RV BV is a candidate jump contribution, not automatically a significance test. Microstructure, irregular −
sampling and observation aggregation can invalidate asymptotic approximations; the diagnostic 
contract must record these limits.
G1_DIFFUSION_JUMP_ROUTE(series):
 validate sampling and observation process
 fit diffusion benchmark
 calculate jump-robust diagnostics where admissible
 compare predictive likelihood against jump alternative
 if jump evidence unstable across reasonable sampling choices:
 return PROCESS_UNRESOLVED
 else return selected process family + uncertainty
38. G1-D: Hawkes estimation and diagnostics
38.1 Univariate exponential Hawkes
λ(t)=μ+Σ_{t_i<t} α exp[−β(t−t_i)], μ>0, α≥0, β>0.
For observation window [0,T] and event times {t_i}, the log-likelihood is the sum of log intensities at 
events minus the integrated intensity.
ℓ(μ,α,β)=Σ_i log λ(t_i) − μT − (α/β) Σ_i [1−exp(−β(T−t_i))].
The branching ratio n=α/β is a derived quantity. For a stationary linear Hawkes interpretation, n<1 is 
required. Values near one are boundary-sensitive and must carry profile-likelihood or bootstrap 
uncertainty.
38.2 Time-rescaling diagnostic
Under a correctly specified conditional intensity, transformed inter-event compensator increments 
should behave as iid Exp(1). Define Λ(t)= _0^t λ(s)ds and z_i=Λ(t_i) Λ(t_{i 1}). The transformed ∫ − −
u_i=1 exp( z_i) should be approximately Uniform(0,1). − −
HAWKES_FIT(events, window):
 initialise multiple feasible parameter starts
 maximise exact log-likelihood under positivity constraints
 reject numerically unstable solutions
 calculate n = alpha/beta with uncertainty
 perform time-rescaling residual tests
 test residual serial dependence
 compare held-out log score with Poisson/count null
 if diagnostics fail or improvement is absent:
 select narrative_null or alternative family
38.3 Multivariate Hawkes
λ_k(t)=μ_k+Σ_j Σ_{t_i^j<t} α_{kj} exp[−β_{kj}(t−t_i^j)].
The matrix of integrated excitation masses A* with elements α_kj/β_kj describes expected offspring 
contribution under the linear model. Stability requires spectral radius ρ(A*)<1 for the stationary 
interpretation. Cross-excitation entries are not causal proof: common unobserved broadcasters can 
generate apparent excitation and must be represented in competing hypotheses.
<PARSED TEXT FOR PAGE: 34 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
38.4 Alternative kernels
Exponential kernels are the default computational benchmark, not a universal law. Power-law, sum-of￾exponentials and non-parametric kernels may be registered when domain evidence supports longer 
memory. Kernel choice is a multiplicity decision and must be nested inside training data.
39. G1-S: source and source-tree inference
Let S be a candidate source set, T_S a directed propagation tree or forest, O the observed 
messages/events, C carrier information and L the point-in-time network. The target posterior is 
proportional to the observation likelihood times source/tree priors.
P(S,T_S|O,C,L) ∝ P(O|S,T_S,C,L) P(T_S|S,L,C) P(S).
The likelihood may factor over observed adoption times conditional on parent candidates when the 
process supports such factorisation. Missing nodes and archival selection require an observation model;
otherwise source certainty will be systematically overstated.
SOURCE_TREE_MODEL_SELECTION(O):
 instantiate H1 single-source cascade
 instantiate H2 independent sources
 instantiate H3 common broadcaster
 instantiate H4 coordinated_activity
 instantiate H5 observation artefact
 for each H:
 integrate/sum over permitted source trees approximately
 include observation-selection model
 compute predictive or marginal score
 return posterior/model weights with uncertainty
 never translate H4 into intent without external evidence
Distributed Ignition DI_t remains diagnostic only. A high DI value can arise from genuine independent 
ignition, an omitted broadcaster, synchronised exposure or observation artefact. It cannot be a 
production predictor until its null and incremental predictive value are established.
40. G1-G: genealogy, mutation and semantic lineage
Narrative units are nodes in a lineage graph rather than independent observations. Let m_i be a 
representation of message i and d(m_i,m_j) a registered semantic or structural distance. Candidate 
parentage is restricted by time and carrier reach.
P(parent=j | child=i) ∝ 1[t_j<t_i] · K_M(j,i,Δt) · exp(−η d(m_i,m_j)).
The semantic distance metric is itself a model component. Embeddings trained on future corpora, later 
editions or post-outcome labels are prohibited. Historical text models must use frozen representations 
or explicitly acknowledge reconstruction leakage and remain development-only.
BUILD_GENEALOGY(messages):
 order by point-in-time availability/reference event
 generate feasible parent set using temporal and network constraints
 score parent candidates using propagation kernel and frozen semantic metric
 retain posterior parent distribution, not only MAP edge
 cluster descendants under ancestry
 prevent descendant count from becoming independent evidence count
<PARSED TEXT FOR PAGE: 35 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
41. G1-I: downstream narrative influence
Virality, systemic influence and transition risk are distinct. A narrative can spread widely without 
changing behaviour; a narrowly distributed message can have high influence if it reaches a structurally 
important node. G1-I therefore requires an outcome-linked response model rather than using cascade 
size as a proxy.
Influence_{M→R}(h) := incremental predictive information of M_t for R_{t:t+h} conditional on 
registered baseline B_t.
No universal influence coefficient is defined. Influence is admitted only through held-out incremental 
scoring against a baseline containing ordinary activity, seasonality and relevant exposure variables.
42. G2: exact OU transition density and estimation
For dX_t= a(X_t μ)dt+σdB_t with a>0, the exact transition over irregular interval Δ is Gaussian. − −
X_{t+Δ}|X_t ~ Normal( μ+(X_t−μ)e^{−aΔ}, [σ /(2a)](1−e^{−2aΔ}) ). ²
This exact transition density is preferred to Euler approximation for the OU benchmark. Parameters 
θ=(a,μ,σ) are estimated by maximising the sum of transition log-likelihoods over the training interval. If 
μ is removed by a predeclared centring transform, that transform is fitted inside the training fold.
FIT_OU(times, x):
 require >= minimum effective observations
 optimise exact irregular-step transition likelihood
 constrain a>0, sigma>0
 inspect profile likelihood for a
 if a near zero or profile flat:
 mark recovery time weakly identified
 use bootstrap for uncertainty
 generate one-step predictive residuals
 test residual whiteness and variance stability
 return parameters + covariance/bootstrap + diagnostics
42.1 Independent diagnostics
D_V = V_emp − σ̂²/(2â).
D_ρ(Δ) = ρ_emp(Δ) − exp(−âΔ).
Because both expectations use fitted parameters, uncertainty propagates through â and σ̂. Diagnostics 
are evidence of model departure only after accounting for estimation covariance and finite-sample 
uncertainty. They are not additional free features.
43. G2: transition signatures and alternative processes
43.1 Saddle-node / critical slowing
The expected signature is loss of restoring strength, increasing recovery time and often increasing 
variance/autocorrelation under restrictive assumptions. The system never treats rising variance alone 
as proof because heteroskedastic forcing, volatility clustering and observation changes can produce the 
same pattern.
<PARSED TEXT FOR PAGE: 36 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
43.2 Flickering
Flickering is represented as switching between locally metastable regimes before a transition. 
Candidate hidden-state models may estimate regime occupancy and switching rates, but the number of 
regimes and emission family are selected inside nested validation.
43.3 Hopf
Re(λ_pair) → 0− with Im(λ_pair)≠0.
A Hopf-compatible claim requires a complex conjugate eigenpair approaching the imaginary axis and 
independently resolvable oscillatory structure. The minimum resolvable frequency separation is of 
order 1/T_window. If the data window cannot resolve the claimed oscillation, the result is 
UNRESOLVED.
43.4 Non-normal amplification
For a linearised system xdot=Ax, asymptotic stability Re eig(A)<0 does not prevent transient growth 
when A is non-normal. The candidate diagnostic is based on ||exp(At)|| or pseudospectral behaviour. 
Such amplification is routed to alternative-process evidence, not automatically to critical transition.
44. G3-L: graph construction and Laplacian inference
Let W_t be a non-negative weighted adjacency matrix after a domain-specific edge construction 
contract. D_t is the diagonal degree/strength matrix. The combinatorial Laplacian is L=D W; the −
symmetric normalised Laplacian is L_sym=I D^{-1/2}WD^{-1/2}. The chosen convention is part of the −
feature definition and cannot change between training and evaluation.
L = D−W; L_sym = I−D^{-1/2} W D^{-1/2}.
For an undirected connected graph, λ_1=0 and λ_2>0. Algebraic connectivity λ_2 approaching zero may 
indicate fragmentation, but graph-size, density and weight-scale changes can alter λ_2 mechanically. 
Comparisons therefore require a frozen normalisation and appropriate graph null.
44.1 Fiedler uncertainty
Rotation_t = 1 − |v_2(t)^T v_2(t−Δ)|.
The absolute inner product removes arbitrary sign flips. When λ_2 and λ_3 are nearly degenerate, v_2 is
unstable and rotation is not interpretable without eigengap information. Davis–Kahan-type bounds 
relate subspace error to perturbation size divided by eigengap.
sin Θ( V, V̂ ) ≤ ||E|| / gap (schematic Davis–Kahan bound under its assumptions).
G3L_UPDATE(W_t):
 validate node set and edge semantics
 apply frozen normalisation
 construct L or L_sym
 compute eigenpairs with numerical tolerances
 estimate edge/measurement perturbation uncertainty
 record eigengaps
 if eigengap too small for vector interpretation:
 suppress Fiedler-vector feature
 emit lambda2, uncertainty, rotation_if_resolved
<PARSED TEXT FOR PAGE: 37 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
45. G3-C: covariance/correlation crowding
For N variables and T effective observations, sample covariance eigenstructure is strongly affected by 
N/T. Random-matrix benchmarks are used only when approximate assumptions are credible. Under a 
simple iid noise benchmark with aspect ratio q=N/T, Marchenko–Pastur support provides a reference 
bulk; real data usually require stronger nulls preserving heteroskedasticity and serial dependence.
λ_± = σ (1 ± √q) (Marchenko–Pastur reference under iid assumptions). ² ²
A leading eigenvalue outside a null bulk is not automatically systemic crowding; common seasonality, 
market beta or measurement synchronisation can create it. BBP-style separation is therefore diagnostic 
and must be compared with domain baselines.
G3C_UPDATE(matrix X):
 standardise using training-only parameters
 estimate effective sample size under serial dependence
 choose registered covariance estimator
 generate appropriate null / RMT reference
 compute eigenvalue separation and eigenvector concentration
 attach uncertainty
 return crowding diagnostics, not causal labels
46. G3-A: exposure-network construction
An exposure network represents potential propagation rather than observed response. Edge w_ij may 
be a physical flow, payment, credit exposure, supply dependency or communication reach. Edge 
semantics must state direction, units, aggregation window and whether the weight is stock, flow, 
probability or intensity.
G_X(t) = {V_X(t), E_X(t), W_X(t)}.
Response networks are separate: G_R(t)={V_R,E_R,W_R}. Similarity between G_X and G_R can be tested 
prospectively, but exposure breadth cannot be substituted for response breadth.
BUILD_EXPOSURE_GRAPH(records, cutoff):
 retain only records available by cutoff
 map entities using versioned identifier table
 aggregate edges with declared window and units
 retain missing vs zero distinction
 attach edge uncertainty and coverage
 produce graph vintage hash
47. G23: master-stability coupling in full
Consider N coupled units x_i with intrinsic dynamics f and coupling output H. For a synchronised 
trajectory s, linearisation in Laplacian eigenmodes gives ηdot_k=[Df(s)+κγ_k DH(s)]η_k. The master￾stability formulation is used only when the domain approximately satisfies the coupling assumptions.
ẋ_i=f(x_i;θ_f)+κ Σ_j L_ij H(x_j;θ_H)+ε_i.
η̇_k=[Df(s)+κγ_k DH(s)]η_k.
Identification requires variation in graph modes and observations sufficient to separate intrinsic 
dynamics from coupling. If κ can trade off almost perfectly against θ_f or edge scaling, the coupling is 
weakly identified.
<PARSED TEXT FOR PAGE: 38 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
47.1 Estimation
ESTIMATE_G23(panel, graph_vintages):
 freeze f family, H family, graph scaling and lag candidates
 split training/validation with embargo
 estimate intrinsic dynamics without coupling
 estimate coupled model under same observation likelihood
 profile kappa and H parameters
 calculate predictive loss difference on inner validation
 run common-driver-preserving surrogate test
 if parameter profile flat OR surrogate invalid:
 TEST_UNRESOLVED
 else freeze candidate and evaluate once on outer holdout
47.2 Null hierarchy
The null hierarchy includes independent block resampling where appropriate, iAAFT for amplitude￾distribution and spectrum preservation, twin surrogates for nonlinear recurrence structure, and 
custom multivariate surrogates preserving common drivers. The least destructive null capable of 
removing the hypothesised coupling is preferred.
The empirical add-one p-value prevents zero p-values from finite surrogate sets. Multiplicity correction 
is applied after registering the coupling family, not after selecting only favourable edges.
48. Dependence testing: HSIC and distance covariance
For samples {(x_i,y_i)}, HSIC measures cross-covariance in reproducing-kernel Hilbert spaces. With 
centred Gram matrices K and L and centring matrix H=I 11ᵀ/n, a common biased estimator is −
proportional to tr(KHLH). Exact normalisation follows the registered implementation.
HSIC_b ∝ tr(K H L H).
Kernel bandwidths are hyperparameters and must be selected within inner folds or by a frozen rule 
independent of outcomes. For time series, null samples must preserve autocorrelation and relevant 
common drivers; ordinary row permutation is invalid.
Distance covariance provides a kernel-free corroborating statistic based on doubly centred pairwise 
distances. Agreement between HSIC and distance covariance is not independent replication if both 
operate on the same observations; it is robustness across statistics.
49. Sequential inference: BOCPD details
BOCPD maintains a posterior over run length r_t, the time since the last changepoint. With changepoint 
prior H(r), the recursion combines growth and reset probabilities.
P(r_t,x_{1:t}) = Σ_{r_{t−1}} P(r_t|r_{t−1}) P(x_t|r_{t−1},x^{(r)}) P(r_{t−1},x_{1:t−1}).
The parameter is named changepoint_rate_prior to avoid collision with transition hazard. Predictive 
distributions are family-specific. The run-length posterior is an observation about regime structure, not 
itself a transition forecast.
BOCPD_STEP(x_t):
 predictive[r] = p(x_t | sufficient_stats[r])
 growth[r+1] = prev[r]*(1-cp_rate[r])*predictive[r]
 reset[0] += prev[r]*cp_rate[r]*predictive[r]
 normalise
<PARSED TEXT FOR PAGE: 39 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 update sufficient statistics for every surviving run length
 prune only by frozen numerical rule
 return run_length_posterior, P(change_at_t)
Warning hysteresis uses separately frozen entry, maintenance, exit, minimum-run and cooldown rules. 
Threshold search occurs inside nested validation and is counted in the hypothesis/model-selection 
ledger.
50. Stage A: feature admission and grouped regularisation
Stage A is responsible for removing invalid and redundant features before outcome modelling. It does 
not grant causal meaning. Features are grouped by G-family, sidecar and ancestry cluster.
min_β L(y,Xβ) + λ1 Σ_g w_g ||β_g||_2 + λ2 ||β||_1.
The sparse-group objective is a candidate implementation allowing group-level and within-group 
sparsity. λ1 and λ2 are selected only inside training data. An ancestry-derived feature can be retained 
for prediction while still counting as the same evidence lineage; predictive utility and evidence 
independence are separate concepts.
STAGE_A(features):
 drop non-F_t-measurable features
 drop unidentified features
 mark deterministic derivatives
 standardise using training-only statistics
 fit candidate sparse-group model inside nested CV
 retain selection stability diagnostics
 pass reduced vector and full ancestry metadata to Stage B
51. Stage B: PLS-Cox and alternatives
51.1 Cox model
h(t|z)=h_0(t) exp(β z). ᵀ
This hazard is statistical. It is not derived from Itô calculus, OU recovery or spectral theory. Those 
components can supply z only after admission. Partial likelihood estimation is used when proportional￾hazards assumptions and censoring structure are appropriate.
L_partial(β)=∏_{i:event} exp(β z_i) / Σ_{j∈R_i} exp(β z_j). ᵀ ᵀ
51.2 PLS projection
Partial Least Squares constructs supervised latent components that maximise covariance with the 
outcome representation. For survival data the exact PLS variant must be declared. The number of 
components is nested-validated and the entire projection is refit within every outer training fold.
PCA is not the default because high-variance directions can be irrelevant to transition risk. 
Conventional penalised Cox, discrete-time logistic hazard and flexible survival models are mandatory 
comparator candidates where data volume supports them.
FIT_STAGE_B(train):
 define comparator set before outer outcome access
 for each candidate:
 nested-select hyperparameters
 test PH assumptions / residual diagnostics
<PARSED TEXT FOR PAGE: 40 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 obtain cross-fitted predictions
 choose by registered loss rule
 refit winner on full outer-training partition
 freeze model object and calibration map
52. Discrete-time event alternative
Where outcomes are naturally evaluated on fixed intervals, a discrete-time hazard may be more 
transparent. For interval k, q_{ik}=P(event in k | survived to k, F_{t_k}). A logistic complementary-log￾log or other registered link can be used.
logit(q_{ik}) = α_k + β z_{ik}. ᵀ
Event probability over a horizon of K intervals is 1 _{k=1}^K(1 q_{ik}). This makes forecast horizons −∏ −
explicit and can simplify Brier evaluation. It remains a statistical calibration layer.
53. Calibration algorithms
Raw model scores are not assumed calibrated. Calibration maps are learned only from 
training/validation predictions generated without in-sample reuse. Candidate maps include 
logistic/Platt-style calibration, isotonic regression where sample size permits, and survival-specific 
calibration procedures.
Binary logistic calibration: logit P(Y=1) = α + β logit(p_raw).
Ideal calibration has α=0 and β=1, but uncertainty must be reported. Isotonic calibration is flexible and 
can overfit small samples, so it requires nested selection and minimum sample/event rules.
CALIBRATE(cross_fitted_predictions, outcomes):
 choose candidate calibrators by preregistered rule
 fit only on predictions not generated in-sample
 evaluate calibration loss in inner validation
 freeze selected map
 apply to untouched outer predictions
54. Proper scoring, discrimination and episode dependence
Brier score and log score are primary probability scores. AUROC may describe ranking but is 
insufficient because it ignores calibration and can look strong under severe class imbalance.
BS = (1/N) Σ_i (p_i−y_i)^2.
LogLoss = −(1/N) Σ_i [y_i log p_i +(1−y_i)log(1−p_i)].
Repeated forecasts of one episode are correlated. The ledger therefore retains forecast-level scores but 
uses episode-clustered uncertainty or non-overlapping evaluation windows for inferential summaries.
54.1 Brier decomposition
Where sample size supports stable binning or nonparametric estimation, Brier score can be 
decomposed into reliability, resolution and uncertainty. The decomposition is descriptive and must not 
be used to tune bins after seeing the result.
54.2 Skill scores
BSS = 1 − BS_PH / BS_baseline.
<PARSED TEXT FOR PAGE: 41 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
A positive BSS is meaningful only with the same outcomes, horizons and target vintages. Comparisons 
across different outcome definitions are invalid.
55. False-alert and lead-time accounting
A warning exists only if a frozen decision rule converts probability/state into a warning. Each warning 
has an issue time, persistence requirement, target episode, horizon and expiry. An expired warning 
without the contracted event is a false alert.
LeadTime = EventStart − FirstValidWarningTime.
Incremental lead time is measured relative to the best relevant recognised leading indicator or 
conventional baseline. If the Psychohistory warning is simply a transformation of that indicator, no new
lead is credited.
RESOLVE_WARNING(w):
 if contracted event occurs within horizon:
 mark TRUE_ALERT
 compute lead time
 elif expiry reached without event:
 mark FALSE_ALERT
 else:
 mark UNRESOLVED
 cluster warnings referring to same episode
56. Historical-anchor distance mathematics
Anchor comparison is deliberately multidimensional. Let state vector s, trajectory descriptor τ, 
propagation descriptor p and evidence-quality descriptor e form A=(s,τ,p,e). Distances are computed 
within domains after training-only scaling.
D_A(i,j) = [D_S(i,j), D_T(i,j), D_P(i,j), D_E(i,j)].
No universal scalar weighting is currently admitted. Candidate scalarisation may use non-negative 
weights learned inside training data, but conventional unweighted or domain-wise kNN must remain a 
comparator.
56.1 State distance
D_S(i,j)=sqrt((s_i−s_j)^T Σ_train^{-1}(s_i−s_j)) (candidate Mahalanobis form).
If Σ is ill-conditioned, shrinkage or diagonal scaling is used according to a frozen rule. Mixed 
categorical/ordinal variables require a mixed-data metric rather than numerical encoding that invents 
interval meaning.
56.2 Trajectory distance
Candidate trajectory comparison may use fixed-lag vector distance or constrained dynamic time 
warping. Unconstrained warping can erase meaningful differences in event speed, so the warping band 
and penalty are preregistered.
D_T = min_{warping path π∈Π} Σ_{(a,b)∈π} c(x_a,y_b) + penalty(π).
<PARSED TEXT FOR PAGE: 42 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
56.3 Uncertainty-aware distance
When anchor components have measurement/reconstruction uncertainty, distance is a distribution 
rather than a point. Monte Carlo propagation draws plausible states from their uncertainty models and 
reports the distribution of D_A. Anchors whose nearest-neighbour status is unstable are downweighted 
or marked unresolved.
ANCHOR_DISTANCE(current, candidate):
 sample/propagate measurement uncertainty
 compute state distance
 compute trajectory distance under frozen alignment rule
 compute propagation-structure distance
 compute evidence-quality mismatch
 return vector distance + uncertainty
57. Anchor retrieval, density and counter-anchors
Nearest historical examples can be misleading in sparse regions. The retrieval engine therefore records 
local anchor density and the distance ratio between nearest neighbours. A 'nearest' case that is 
absolutely distant is not treated as close merely because nothing better exists.
Counter-anchors are deliberately retrieved alongside recurrence anchors. If pre-outcome states are 
similar but post-outcomes diverge, the pair is evidence that an omitted variable, stochasticity or regime 
difference matters.
D_pre(i,j) small ∧ D_post(i,j) large ⇒ divergence/counter-anchor candidate.
RETRIEVE_ANCHORS(q):
 find candidates using only each anchor's pre-outcome information
 retrieve R/T anchors
 retrieve F/N/D/C counterexamples from comparable distance shell
 estimate local density
 compute uncertainty-aware distance
 produce neighbour set without outcome-dependent re-ranking
58. Cycle and motif testing
A cycle family is admitted only after distinguishing periodicity from recurrence. Periodicity asks 
whether a process has stable frequency structure; recurrence asks whether states or sequences revisit 
similar regions without fixed period.
58.1 Periodicity
Spectral tests require stationarity assumptions or local windows and multiple-testing correction across 
frequencies. A visually attractive historical interval is not evidence.
58.2 Quasi-cycle
Quasi-cycles may arise from stochastic excitation of damped modes. They require comparison with 
stochastic linear/nonlinear nulls rather than deterministic cycle fitting.
58.3 Sequence recurrence
P(X_{t+h}|X_{t−w:t}) vs P(X_{t+h}|baseline information).
<PARSED TEXT FOR PAGE: 43 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
Predictive recurrence is established only if trajectory-neighbour information improves held-out scoring.
The historical kNN baseline is mandatory; if it performs as well as the elaborate atlas, the atlas is 
unnecessary.
58.4 Phase
A phase φ_t is defined only for systems with empirically identifiable cyclic structure. Hilbert-transform 
or state-space phase estimates are candidate methods; phase is forbidden for merely narrative 'cycles'.
59. Shock geometry and transmission response
Shock Geometry SG=[magnitude,speed,persistence,breadth,cross-domain response] separates source 
characteristics from propagation. Magnitude may be standardised Δx/σ_Δx using a training-only 
volatility estimate.
SG_t = [Δx_t/σ̂_Δx, v_t, persistence_t, breadth_t, response_vector_t].
Transmission Response TR records how receiving nodes respond after accounting for exposure and 
buffers. Stress Absorption SA_i,t=ΔResponse_i/(ΔStress+ε) remains conceptual until numerator, 
denominator and ε have domain-specific semantics.
Cross-asset or cross-sector response remains a vector [rates,credit,equity,flows,energy,FX,regional,…] 
rather than being averaged into a universal stress number.
60. Sidecar: BADL / BADL-M markets
BADL is a market-domain sidecar. Its purpose is to detect unusual configurations in liquidity, spread, 
crowding, narrative and cross-asset response without converting every anomaly into systemic hazard.
The legacy multiplicative outlier score O=(S^.30 C^.20 N^.15 T^.15 A^.20)/(R^.60 F^.40) is retained only as
a candidate handcrafted model. Its exponents are design choices. It must compete against simpler z￾score, Mahalanobis, robust covariance and supervised baselines.
BADL_CYCLE:
 ingest point-in-time market prices/volumes/spreads/flows
 separate market microstructure from macro variables
 construct operator-specific covariance/exposure diagnostics
 run transform-ancestry gate
 compute candidate anomaly models
 if Outcome Contract exists:
 compare against volatility/persistence/conventional stress baselines
 output Signal|Vector|Hazard only where calibrated
61. Sidecar: GISC geopolitical instability
GISC represents observable geopolitical instability without inferring hidden intent. Inputs can include 
event counts, mobilisation, sanctions, trade disruption, official actions and network exposure, each with
source-quality and reporting-bias models.
Media attention is not event incidence. Repeated syndicated reports are ancestry-linked. Country 
observations sharing one international source are not independent confirmations.
GISC:
 separate event occurrence from reporting intensity
<PARSED TEXT FOR PAGE: 44 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 geolocate with uncertainty
 construct exposure network separately from response network
 register escalation outcomes prospectively
 compare against simple event-count and persistence baselines
62. Sidecar: CTSC climate transition
CTSC separates physical hazards, policy transition, energy-system changes, insurance/financial 
exposure and behavioural response. Weather observations are not climate trends; policy 
announcements are not implementation; asset repricing is not physical damage.
Temporal scales are explicitly heterogeneous. A short-run shock model and long-run transition model 
cannot share a horizon label merely because both are 'climate'.
63. Sidecar: TPSS technological phase shift
TPSS models adoption, investment, capability, substitution and institutional response to technological 
change. Patent counts, venture funding, benchmark capability and product adoption are distinct 
observation processes.
Technology substitution requires the Substitution Awareness decomposition. Growth in one technology 
and decline in another can be one transition rather than two independent signals.
64. Sidecar: CCSC corporate collapse
CCSC distinguishes market-implied distress, accounting deterioration, liquidity stress, refinancing 
exposure, supplier/customer propagation and formal insolvency. Credit spreads and equity drawdowns 
share market ancestry and cannot automatically be counted as independent.
A corporate-collapse outcome must specify legal/operational event definition and horizon. 'Trouble' is 
not an outcome contract.
65. Sidecar: SCFS supply-chain fracture
SCFS uses directed exposure networks, inventory/buffer information, transport constraints and 
response observations. Payment-network data are potentially useful exposure evidence but payment 
value equals a mixture of price, quantity, timing and contract structure.
PaymentValue_ij,t ≈ Price_ij,t × Quantity_ij,t × TimingFactor_ij,t × ContractFactor_ij,t.
Therefore payment spikes are not physical-flow estimates without additional identification. SCFS must 
benchmark network features against commodity prices, conventional freight indicators and sector 
activity measures.
66. Candidate domain: infectious-disease outbreak
The outbreak domain is not a production sidecar yet. It requires separate observation models for 
laboratory confirmations, syndromic surveillance, hospitalisation, mortality, testing policy, wastewater, 
mobility and commercial activity.
<PARSED TEXT FOR PAGE: 45 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
ObservedCases_t = Incidence_t × DetectionProbability_t + reporting/error process.
Detection probability changes with testing availability, case definition and behaviour. Commercial 
spending or mobility can respond to both disease and policy, creating common-driver confounding. 
Outbreak forecasts therefore require explicit epidemiological baselines; Psychohistory must outperform
them rather than merely rediscover epidemic growth.
OUTBREAK_CANDIDATE:
 define pathogen/event outcome
 reconstruct surveillance vintages
 model testing/detection changes
 use epidemiological baseline (renewal/SEIR/etc.) appropriate to task
 add network/memetic/commercial features only incrementally
 score prospective probabilities and peak/timing outcomes separately
67. Candidate domain: banking, lending and property
Banking and housing variables are strongly linked by recognised mechanisms and recognised leading 
indicators. Mortgage approvals, rates, credit standards, transactions, listings, construction and prices 
occupy different points in the pipeline.
The minimum housing benchmark ladder is price persistence mortgage approvals approvals+rates → →
→ → minimal conventional multivariate model Psychohistory additions. Approvals cannot be consumed 
by PH and then omitted from the baseline.
Property-price outcomes require target-vintage declaration because indices are revised and measure 
different transaction populations.
68. Candidate domain: gold, pensions and cultural activity
Gold purchasing can reflect inflation expectations, reserve management, geopolitical hedging, currency 
risk, portfolio flows or local cultural demand. A rise in gold demand cannot be assigned a single motive. 
Central-bank purchases, ETF flows, futures positioning and retail demand require separate observation 
processes.
Pension contribution, withdrawal, transfer and asset-allocation changes similarly mix demographic, 
tax, income, regulatory and market mechanisms. 'Pension increase/decrease' is not a sufficiently 
defined variable until the exact flow or stock is specified.
Arts/cultural rise and decline requires operational outcomes such as attendance, ticket revenue, 
production counts, employment, venue openings/closures, publication, streaming or funding. Media 
prominence is not cultural participation. Historical reconstruction must explicitly model survivorship 
because successful works are disproportionately preserved.
69. Candidate domain: hostility and violence toward disabled 
people
This domain requires especially strict observation-process separation. Police-recorded hate crime, 
prosecutorial charges, victimisation surveys, service-provider reports, online abuse and news coverage 
measure different processes. Changes in law, reporting propensity and recording practice can create 
structural breaks.
<PARSED TEXT FOR PAGE: 46 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
Recorded_t = f(Incidence_t, Reporting_t, Recording_t, LegalDefinition_t, Enforcement_t, 
Classification_t).
No scalar 'disability hostility' index is admitted. A future research vector may retain recorded events, 
victimisation evidence, media visibility, online expression and institutional environment separately. 
News volume is never treated as incidence.
The domain is used to test measurement architecture, not to profile individuals or infer protected￾characteristic risk from personal data.
70. Causal language and mechanism discipline
Psychohistory is primarily predictive. Causal claims require additional identification assumptions. 
Temporal precedence plus dependence is insufficient. Directed network arrows in exposure diagrams 
denote hypothesised transmission direction, not proven causal effects.
Where causal estimation is attempted, the identification strategy must be explicit: natural experiment, 
instrumental variable, difference-in-differences, synthetic control, structural model or another 
defensible design. Such estimates remain separate from ordinary predictive edges.
Predictive edge: ΔLoss_OOS(A→B | baseline) < 0. Causal edge: requires an identification 
argument beyond prediction.
71. Missingness, censoring and data defects
Missing values are classified as structural, not-yet-released, source outage, suppressed, not applicable or
genuinely unknown where possible. Future backfill is prohibited. Imputation models are trained only 
on the available past and carry an imputation indicator/uncertainty.
Outcome censoring is handled according to the survival/discrete-time model. Ambiguous event dates 
follow the Outcome Contract's ambiguity policy rather than analyst discretion after seeing predictions.
MISSINGNESS_GATE(value):
 classify missingness reason
 if not-yet-released:
 keep missing at historical forecast origin
 if imputable under frozen rule:
 impute using training-only model
 attach imputation flag/uncertainty
 else:
 route model to missing-aware path or exclude feature
72. Normalisation and cross-era comparability
Cross-era normalisation is allowed only for quantities whose semantics survive the transform. 
Standardisation within an era can align scale but cannot make institutions, carriers or legal categories 
equivalent.
z_{i,t}=(x_{i,t}−μ_{era,i})/σ_{era,i} is a scale transform, not proof of construct equivalence.
Carrier-relative memetic time τ_M=(t t0)/T_medium is similarly a comparison aid. It cannot normalise −
away printing, broadcast or digital-network topology.
<PARSED TEXT FOR PAGE: 47 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
73. Uncertainty propagation
Psychohistory distinguishes measurement, parameter, model, source, reconstruction, distance, outcome
and sampling uncertainty. A single confidence score is prohibited unless a validated aggregation exists.
For smooth transforms y=f(θ), delta-method covariance JΣJᵀ may be used away from boundaries. 
Bootstrap, posterior simulation or Monte Carlo propagation is preferred for boundary-sensitive, 
nonlinear and historical-reconstruction problems.
PROPAGATE_UNCERTAINTY(component):
 if analytic regularity credible:
 use analytic covariance/delta method
 elif resampling preserves dependence structure:
 use registered bootstrap
 elif probabilistic reconstruction available:
 Monte Carlo from reconstruction/posterior
 else:
 mark uncertainty PARTIAL/UNQUANTIFIED
 prohibit precision-dependent promotion
74. Identifiability
A parameter is not considered identified merely because an optimiser returns a number. Diagnostics 
include profile likelihood curvature, posterior concentration where Bayesian methods are used, 
sensitivity to initialisation, parameter trade-offs and simulation recovery.
IDENTIFIABILITY_AUDIT(model):
 run multi-start estimation
 compute/profile objective over key parameters
 inspect Hessian/condition number where meaningful
 perform simulation-recovery on fitted scale
 perturb observation window and reasonable preprocessing
 if parameter changes exceed declared tolerance or profile is flat:
 mark WEAKLY_IDENTIFIED
Weak identification blocks mechanistic interpretation and can block predictive admission when 
predictions are unstable. Stable predictions from unstable parameters may still be usable as black-box 
prediction if prospectively validated, but the mechanism claim remains withheld.
75. Simulation-based calibration and synthetic tests
Synthetic data are used for algorithm verification, not empirical validation. Every synthetic result is 
labelled synthetic. Simulation tests ask whether the implementation recovers known parameters, 
controls false positives under nulls and detects signals at plausible effect sizes.
SIMULATION_TEST_SUITE:
 null diffusion with no transition
 OU with known recovery parameter
 jump process
 Hawkes with n well below 1 and near 1
 fragmented vs stable graph
 common-driver pseudo-coupling
 true coupled system
 recurrent historical trajectories with and without predictive value
 revision/vintage leakage trap
<PARSED TEXT FOR PAGE: 48 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 ancestry-duplication trap
Passing simulation tests establishes implementation correctness under the simulated assumptions. It 
does not establish that real systems obey those assumptions.
76. Multiplicity ledger in full
Multiplicity arises from variables, transforms, lags, horizons, geographies, graph operators, kernels, 
model families and repeated analyst cycles. Every searched degree of freedom belongs in the registry 
even when the corresponding result is negative.
Family size ≠ number of reported significant tests; it is the number of hypotheses actually 
searched under the declared family.
Outer holdout evaluation is treated as one registered result per frozen model/outcome contract. 
Analysts may inspect errors after evaluation, but any subsequent change creates a new model version 
and the inspected holdout becomes development-exposed.
77. Nested validation and temporal splitting
Random k-fold cross-validation is generally inappropriate for temporally dependent forecasting. 
Psychohistory uses rolling or blocked temporal splits with embargo. Hyperparameters, feature 
selection, calibration and lag selection occur only inside the outer training segment.
NESTED_TEMPORAL_CV(data):
 for outer split k:
 train_outer = data before test_k minus embargo
 test_outer = frozen future block
 for inner temporal splits inside train_outer:
 tune preprocessing, lags, regularisation, model, calibration
 freeze selected pipeline
 predict test_outer once
 concatenate outer predictions for development estimate
Development cross-validation is still development evidence. The final lockbox remains untouched until 
the complete pipeline and decision rules are frozen.
78. Baseline library
The baseline library is not a token comparator. It is deliberately strong enough to falsify unnecessary 
complexity.
Class Examples
Base rate historical event frequency within training data
Persistence last state / no-change / random-walk where 
appropriate
Seasonal seasonal naïve, calendar-conditioned rate
Time series AR/ARIMA/state-space/ETS as appropriate
Volatility GARCH/realised-volatility baseline for market 
tasks
<PARSED TEXT FOR PAGE: 49 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
Epidemiology renewal/SEIR-family baseline for outbreak tasks
Leading indicator mortgage approvals, new orders, recognised 
external forecast
Minimal multivariate small penalised/logistic/survival model
Historical recurrence ordinary kNN without PH atlas machinery
The exact baseline is domain-specific. Psychohistory does not earn skill by beating a deliberately weak 
straw model.
79. Model comparison and uncertainty
Differences in proper scores are reported with uncertainty appropriate to temporal/episode 
dependence. Block bootstrap or episode bootstrap may be used when assumptions are defensible. A tiny
mean improvement with an interval spanning material harm is not grounds for promotion.
ΔS = S_PH − S_baseline; promotion requires the registered direction of improvement and 
adequate uncertainty evidence.
No universal p-value threshold is imposed for predictive comparison; the decision rule is specified per 
experiment and includes practical effect size, uncertainty and replication.
80. Promotion, demotion and deletion rules
PROMOTION_GATE(candidate):
 require measurement validity
 require identifiability sufficient for intended claim
 require multiplicity-corrected/replicated dependence where relevant
 require prospective or untouched held-out improvement
 require improvement over inherited external information baseline
 require no leakage or invalid null
 if all pass: ADMITTED
 else remain CANDIDATE/UNRESOLVED
DEMOTION_GATE(admitted_component):
 if repeated preregistered ablations show no value
 OR revision robustness fails
 OR source methodology invalidates measurement
 OR calibration degrades materially:
 demote and version the specification
DELETE:
 remove algebraic duplicate, invalid construct or persistently useless machinery
 preserve historical record of deletion
81. Complete raw-data-to-forecast operator
The complete production mapping is a composition of versioned operators. No arrow may be 
implemented as an undocumented analyst judgement.
D_{≤t}^{(v)} → O_t → T_E → Φ_G1,Φ_G2,Φ_G3,Φ_G23 → Φ_sidecars → A_t → Z_t → f_θ → c → 
P(Y_{t:t+h}=1).
<PARSED TEXT FOR PAGE: 50 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
D is the vintage store; O the measurement-valid observations; T_E the ancestry graph; Φ are feature 
operators; A historical-anchor information; Z the admitted predictor vector; f_θ the frozen predictive 
model; c the frozen calibration map.
FORECAST(t, contract):
 D = realtime_store.snapshot(t)
 O = measurement_layer.validate(D)
 TE = ancestry_layer.update(O)
 G1 = g1_pipeline(O, TE)
 G2 = g2_pipeline(O, TE)
 G3 = g3_pipeline(O, TE)
 G23 = g23_pipeline_if_valid(G2, G3, O, TE)
 S = sidecar_pipeline(O, TE)
 A = anchor_pipeline(G1, G2, G3, S, t)
 Z = admission_layer.assemble(G1,G2,G3,G23,S,A)
 raw = frozen_model[contract].predict(Z)
 p = frozen_calibrator[contract](raw)
 baselines = baseline_library.predict(contract, O)
 ledger.write_before_outcome(t, contract, p, baselines, all_vintages, model_hash)
 return p
82. Evaluation-cycle algorithm with no-future-leakage proof 
obligations
Every cycle emits a machine-readable audit alongside the human report. The audit records the 
maximum availability timestamp consumed, model hash, source-vintage manifest, hypothesis-registry 
snapshot and outcome-resolution state.
EVALUATION_CYCLE(now):
 assert all consumed observations availability_time <= now
 snapshot registries and model hashes
 ingest new releases
 update only features whose parents changed
 run measurement/ancestry audits
 issue forecasts for active contracts BEFORE resolving later outcomes
 resolve outcomes whose authoritative release is now available
 score frozen historical forecasts only
 run baseline comparisons and ablations
 record failures and unresolved tests
 allow specification proposal, but never rewrite historical forecasts
 mark all inspected data DEVELOPMENT_EXPOSED where applicable
A cycle that changes a model and then evaluates the changed model on an outcome already inspected is 
development analysis, not prospective validation. The ledger must preserve that distinction 
permanently.
83. Reproducibility manifest
RunManifest:
 run_id
<PARSED TEXT FOR PAGE: 51 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 timestamp
 code_commit
 environment_lock_hash
 random_seeds
 source_vintage_manifest
 observation_schema_version
 outcome_contract_versions
 hypothesis_registry_hash
 feature_contract_hash
 model_hash
 calibration_hash
 baseline_hashes
 output_hashes
The manifest is sufficient to establish what the system knew and what code produced the forecast. If an 
external source cannot be archived for licensing reasons, the manifest stores its identifier, timestamp, 
checksum where possible and extraction procedure.
84. Database schema
Table Key fields
observations observation_id, variable_id, reference interval, 
availability, vintage, value, units
sources source_id, URI/identifier, method version, 
authority, retrieval metadata
ancestry_edges parent_id, child_id, relation_type, 
confidence/notes
feature_contracts feature_id, parents, transform, role, lookback, 
uncertainty rule
hypotheses hypothesis_id, family, variables, lags, null, status, 
p/q
outcome_contracts event definition, horizon, source, vintage, 
ambiguity, expiry
forecasts issue time, probability, model hash, contract, 
baselines, vintages
outcomes contract, episode, resolved value, vintage, 
resolution time
anchors anchor id, pre-outcome representation, 
uncertainty, class
model_versions hash, training range, configs, promotion status
evaluation_runs run manifest, metrics, failures, change proposals
85. API-level contracts
ObservationProvider.snapshot(cutoff) -> ObservationSet
<PARSED TEXT FOR PAGE: 52 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
MeasurementValidator.validate(ObservationSet) -> ValidatedObservationSet
AncestryGraph.update(ValidatedObservationSet) -> EvidenceGraph
FeatureOperator.transform(data, cutoff, fitted_state) -> FeatureBundle
Sidecar.run(data, cutoff) -> {Signal, Vector, Hazard?}
AnchorEngine.retrieve(state, cutoff) -> AnchorBundle
Predictor.predict(features, contract) -> RawRisk
Calibrator.transform(raw_risk) -> Probability
Ledger.issue(record) -> immutable ForecastID
OutcomeResolver.resolve(contract, now) -> Outcome|UNRESOLVED
Scorer.score(forecasts,outcomes,baseline) -> MetricBundle
Immutable forecast records are essential. Corrections create linked superseding records but never erase
the original issued probability.
86. Unit and integration test requirements
 Exact-vintage test: later revisions must not appear in historical snapshots.
 Ancestry test: deterministic transforms share parent lineage and cannot increase evidence breadth.
 OU recovery test: simulated parameters recovered within declared tolerance under adequate 
sample.
 Hawkes null test: Poisson data must not systematically generate self-excitation after correction.
 Graph convention test: λ2 and node ordering invariant under node relabelling.
 Fiedler sign test: rotation invariant to eigenvector sign.
 Coupling confounder test: common-driver surrogate prevents false edge promotion.
 Outcome-contract test: ambiguous or late outcomes follow frozen policy.
 Forecast immutability test: issued probabilities cannot be overwritten.
 Embargo test: effective lookback never crosses into outer test data.
 Calibration test: calibrator never trains on its own prediction targets.
 Anchor leakage test: post-outcome historical information excluded from anchor representation.
 Multiplicity test: all searched lags/horizons enter family accounting.
 Missing-release test: historical snapshot preserves not-yet-released missingness.
87. Current admission matrix
Object Mathematics Implementation 
status
Predictive admission
G1 diffusion/jump specified implementable not globally admitted
G1 Hawkes specified implementable domain-specific 
candidate
G1 source tree specified framework likelihood domain￾specific
candidate
G1 genealogy specified framework metric domain-specific candidate
G2 OU specified exact 
likelihood
implementable diagnostic candidate
G2 Hopf/flicker specified criteria domain-specific candidate
G3-L specified implementable candidate
<PARSED TEXT FOR PAGE: 53 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
G3-C specified implementable with 
nulls
candidate
G3-A specified interface domain-specific graphs candidate
G23 specified contract conditional none promoted
HSIC/dCov specified implementable candidate tests
BOCPD specified implementable candidate
PLS-Cox specified default implementable not proven superior
Anchor engine specified implementable must beat kNN
Sidecars interfaces specified domain modules 
partial
no universal admission
Aggregate PH skill scoring specified ledger immature UNMEASURED
88. Prospective research programme
The research programme is staged to prevent architecture growth from outrunning evidence. Phase 1 
completes the immutable real-time data and forecast ledger. Phase 2 registers a small set of outcome 
contracts with strong baselines. Phase 3 evaluates single G-families and sidecars. Phase 4 permits 
interactions only after marginal components show value. Phase 5 evaluates historical anchors and 
cross-domain recurrence against ordinary kNN. Phase 6 considers broader integration only if the earlier
phases demonstrate incremental skill.
The first objective is not a universal social forecast. It is a set of narrow, auditable predictions whose 
successes and failures can be accumulated without rewriting history.
89. Normative checklist for every new variable
NEW_VARIABLE_CHECKLIST:
 What exactly is observed?
 What are its units and scale semantics?
 What process produced it?
 What is its reference interval?
 When was it actually available?
 Is it revised?
 Is composition stable?
 What is its observation horizon?
 What are its ancestry parents?
 Is it algebraically derived?
 What uncertainty is known?
 Is it identifiable for the proposed interpretation?
 What simple baseline already contains this information?
 What outcome and horizon could test incremental value?
 What multiplicity family does the test enter?
90. Normative checklist for every claimed relationship
RELATIONSHIP_CHECKLIST:
<PARSED TEXT FOR PAGE: 54 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 Was the relationship declared before outcome inspection?
 Are A and B independently measured enough for the claim?
 Is temporal ordering genuine under publication vintages?
 Is the lag fixed or nested-selected?
 Are common drivers represented in the null/baseline?
 Is the test valid under serial dependence?
 Is multiplicity corrected?
 Has it replicated?
 Does it improve held-out prediction?
 Is the claim predictive or causal?
 Are downstream edges being inferred without tests?
91. Normative checklist for every historical analogy
HISTORICAL_ANALOGY_CHECKLIST:
 Is only pre-outcome information used?
 Is archival survivorship modelled?
 Are carrier and network differences retained?
 Are scale semantics comparable?
 Is source uncertainty represented?
 Are counter-anchors retrieved?
 Is similarity absolute enough to be meaningful?
 Does the analogy improve prediction over kNN/base rates?
 Was the historical case selected before seeing the target outcome?
92. Normative checklist for every published score
SCORE_CHECKLIST:
 Was the forecast immutable before outcome?
 Is the Outcome Contract version frozen?
 Is target vintage correct?
 Is the outcome mature?
 Are repeated forecasts clustered by episode?
 Is the same sample used for PH and baseline?
 Is uncertainty reported?
 Was calibration trained without leakage?
 Are false alerts expired rather than merely unresolved?
 Is lead time incremental over inherited leading information?
93. Failure-state vocabulary
State Meaning
VALID contract satisfied
EXPLORATORY_ONLY useful for research, barred from production 
prediction
WEAKLY_IDENTIFIED parameter/construct not stably identified
PROCESS_UNRESOLVED competing process families not separable
SOURCE_UNRESOLVED source/source-tree posterior insufficiently 
concentrated
<PARSED TEXT FOR PAGE: 55 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
TEST_UNRESOLVED null/test invalid or insufficient power
REVISION_UNSTABLE real-time interpretation changes materially 
across vintages
ANCESTRY_REDUNDANT not independent evidence
HORIZON_UNRESOLVED semantic/forecast horizon unclear
OUTCOME_UNRESOLVED event has not matured
DEVELOPMENT_EXPOSED outcome/data inspected during design
ADMITTED passed declared predictive gate
94. What would count as success
Success is not a compelling retrospective explanation. A successful Psychohistory component must 
improve a proper score on untouched or genuinely prospective outcomes, retain calibration, avoid 
unacceptable false-alert burden, and add lead or discrimination beyond the strongest simple baseline 
that already contains inherited information.
System-level success requires replication across more than one episode and preferably more than one 
domain without silently changing definitions. The framework should become simpler, not more 
elaborate, when components fail.
95. What would count as failure
Psychohistory 2.4 fails in its stronger form if the additional G-family, network, anchor and sidecar 
structure does not improve prospective predictions over conventional baselines after adequate sample 
accumulation. It also fails if apparent skill disappears under real-time vintages, ancestry correction or 
proper multiplicity control.
A failure result is scientifically useful. The architecture explicitly permits deletion until only empirically
useful components remain.
96. Frozen empirical status at this storage revision
As of 6 October 2026, the architecture is substantially specified but aggregate predictive performance is 
not demonstrated. No legitimate overall Psychohistory Brier score, calibration slope, false-alert rate or 
incremental lead-time advantage exists yet. No G23 coupling has been promoted. Current and historical 
observations inspected during development are not retroactive forecasts.
This status statement is normative and must remain attached to the specification until prospective 
ledger evidence changes it. Future editions may update the status, but must preserve this edition and its
forecast history.
97. Full implementation sequence
BUILD_SEQUENCE:
 01 create immutable vintage store
 02 implement ObservationRecord and source registry
<PARSED TEXT FOR PAGE: 56 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 03 implement Evidence Ancestry Graph
 04 implement Outcome Contracts and Forecast Ledger
 05 implement baseline library first
 06 implement scoring and episode resolution
 07 implement G2 OU + diagnostics
 08 implement G1 process dispatch + Hawkes/jump models
 09 implement G3-L/C/A operator-specific modules
 10 implement surrogate registry and dependence tests
 11 implement BOCPD and hysteresis
 12 implement Stage A admission/redundancy gates
 13 implement Stage B candidate predictors/calibration
 14 implement historical anchor store and kNN baseline
 15 implement uncertainty-aware anchor engine
 16 implement sidecars one domain at a time
 17 implement G23 only after G2/G3 single-family validation
 18 begin prospective forecast issuance
 19 freeze lockbox
 20 evaluate; ablate; delete failures
The ordering is intentional. Building sophisticated network coupling before the vintage ledger, baselines
and immutable forecast system would optimise the least important part first and make leakage difficult 
to detect.
98. Canonical end-to-end pseudocode
INITIALISE():
 load versioned schemas
 load frozen outcome contracts
 load hypothesis and multiplicity registries
 load feature contracts and sidecar configs
 verify no lockbox access
 verify source clocks
AT EACH EVALUATION TIME t:
 snapshot = realtime_store.snapshot(t)
 validated = measurement.validate(snapshot)
 ancestry = evidence_graph.update(validated)
 g1d = G1.process_dispatch(validated)
 g1s = G1.source_inference(validated, g1d)
 g1g = G1.genealogy(validated, g1s)
 g1i = G1.influence_candidates(validated, g1d, g1s, g1g)
 g2 = G2.local_stability(validated)
 g3l = G3.laplacian(validated)
 g3c = G3.covariance(validated)
 g3a = G3.exposure(validated)
 g23 = G23.run_only_if_contract_passes(g2,g3l,validated)
 deps = dependence_registry.update(validated)
 seq = sequential_detectors.update(validated)
 sidecar_vectors = []
 for sidecar in enabled_sidecars:
<PARSED TEXT FOR PAGE: 57 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 sidecar_vectors.append(sidecar.run(validated, ancestry))
 current_state = assemble_state_without_scalar_collapse(
 g1d,g1s,g1g,g1i,g2,g3l,g3c,g3a,g23,deps,seq,sidecar_vectors
 )
 anchors = anchor_engine.retrieve(
 current_state,
 historical_store,
 pre_outcome_only=True,
 include_counteranchors=True
 )
 candidates = feature_contracts.evaluate(current_state, anchors)
 admitted = admission_gate(candidates, ancestry)
 for outcome_contract in active_contracts(t):
 baseline_predictions = baselines.predict(outcome_contract, validated)
 raw_prediction = frozen_predictor[outcome_contract].predict(admitted)
 probability = frozen_calibrator[outcome_contract](raw_prediction)
 forecast_ledger.issue_immutable(
 t=t,
 information_cutoff=t,
 probability=probability,
 baselines=baseline_predictions,
 outcome_contract=outcome_contract,
 vintages=snapshot.manifest,
 model_hash=current_model_hash
 )
 matured = outcome_resolver.resolve_available(t)
 metrics = scorer.update_only_frozen_forecasts(matured)
 audit = failure_auditor.run(
 leakage=True,
 redundancy=True,
 identifiability=True,
 multiplicity=True,
 calibration=True,
 revision_robustness=True,
 null_validity=True
 )
 write_run_manifest(t, metrics, audit)
99. Final normative statement
Psychohistory 2.4 is defined by the combination of its forecasting machinery and its restrictions. 
Removing the point-in-time vintage requirement, ancestry accounting, multiplicity registry, edge-local 
validation, strong baselines, immutable forecast ledger or prospective scoring would produce a 
different and substantially weaker system even if the same equations remained.
<PARSED TEXT FOR PAGE: 58 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
The framework is intentionally capable of returning UNRESOLVED. That is not a software error. In 
complex social systems, refusing to convert inadequate evidence into a numerical claim is part of the 
algorithm.
This specification is the canonical 2.4 mathematical and algorithmic storage revision dated 6 October 
2026. Later empirical results must be appended through versioned evaluation records; they must not 
rewrite the assumptions, forecasts or evidence state that existed at this date.
Appendix E. Algorithm index
1. 1. MEASUREMENT_QUALITY
2. 2. RECONSTRUCT_REAL_TIME_PANEL
3. 3. REDUNDANCY_GATE
4. 4. G1_DIFFUSION_JUMP_ROUTE
5. 5. HAWKES_FIT
6. 6. SOURCE_TREE_MODEL_SELECTION
7. 7. BUILD_GENEALOGY
8. 8. FIT_OU
9. 9. G3L_UPDATE
10. 10. G3C_UPDATE
11. 11. BUILD_EXPOSURE_GRAPH
12. 12. ESTIMATE_G23
13. 13. DEPENDENCE_TEST
14. 14. BOCPD_STEP
15. 15. STAGE_A
16. 16. FIT_STAGE_B
17. 17. CALIBRATE
18. 18. RESOLVE_WARNING
19. 19. ANCHOR_DISTANCE
20. 20. RETRIEVE_ANCHORS
21. 21. BADL_CYCLE
22. 22. GISC
23. 23. OUTBREAK_CANDIDATE
24. 24. MISSINGNESS_GATE
25. 25. PROPAGATE_UNCERTAINTY
26. 26. IDENTIFIABILITY_AUDIT
27. 27. SIMULATION_TEST_SUITE
28. 28. NESTED_TEMPORAL_CV
29. 29. PROMOTION_GATE
30. 30. FORECAST
31. 31. EVALUATION_CYCLE
32. 32. NEW_VARIABLE_CHECKLIST
33. 33. RELATIONSHIP_CHECKLIST
34. 34. HISTORICAL_ANALOGY_CHECKLIST
35. 35. SCORE_CHECKLIST
36. 36. BUILD_SEQUENCE
37. 37. INITIALISE / canonical end-to-end loop
<PARSED TEXT FOR PAGE: 59 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
Appendix F. Canonical principles and prohibitions
 An unquantified, unidentified or unvalidated quantity is not yet a measurement.
 Distinct labels do not imply independent evidence.
 A locally valid/significant result is not automatically a globally valid discovery.
 Historical resemblance is conditional evidence, never destiny.
 Current state is not future hazard.
 A shock is not exposure, and exposure is not response.
 Publication lead is not necessarily phenomenon lead.
 Current state, momentum, pipeline and expectations retain separate horizon semantics.
 Different transforms of one source do not become independent observations.
 Different organisations can triangulate measurement without creating independent causal 
evidence.
 Predictive coupling is not causal proof.
 Evidence for A B does not validate B C. → →
 No spectral claim without a resolution bound.
 No forecast score without a frozen event definition and horizon.
 No final-vintage history in a real-time backtest unless final vintage is the declared target.
 No retrospective success credit for a forecast that was never issued.
 No external forecast or recognised leading indicator may be consumed without becoming a 
baseline.
 No scalar composite is required where the evidence is genuinely multidimensional.
 No intent is inferred from coordinated patterns without evidence.
 October 2026 remains development-exposed.
 Aggregate OOS skill remains unmeasured until the prospective ledger matures.
<PARSED TEXT FOR PAGE: 60 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
Part III — Derivations, Contracts, Test Protocols and Storage 
Appendices
Part III removes the remaining implementation ambiguity. It expands derivations, data contracts, 
domain-specific nulls, simulation protocols, scoring reports, and storage rules. It does not add empirical 
claims.
100. Itô calculus reference and permitted use
For an Itô process dX_t=μ(X_t,t)dt+σ(X_t,t)dB_t and twice differentiable f(X,t), Itô's formula gives the 
stochastic differential of Y_t=f(X_t,t).
df = (∂_t f + μ∂_x f + 1/2 σ ∂_{xx}f)dt + σ∂_x f dB_t. ²
The second-derivative term is the defining correction produced by quadratic variation. Psychohistory 
uses this machinery only when transforming stochastic state variables or constructing counter-models. 
It does not use Itô's formula to derive social transition hazards.
100.1 Geometric Brownian motion
dS_t=μS_tdt+σS_tdB_t.
d log S_t=(μ−σ /2)dt+σdB_t. ²
GBM is a benchmark for positive multiplicative processes. Its log increments are conditionally Gaussian 
with variance proportional to elapsed time. Empirical heavy tails, jumps, stochastic volatility and mean 
reversion can invalidate it; failure of GBM is model-departure evidence, not transition evidence.
100.2 Black–Scholes counter-model
∂_t V + 1/2 σ S ∂_{SS}V + rS∂_S V − rV = 0. ² ²
The Black–Scholes PDE may be used as a market counter-model when an option-pricing residual is 
meaningful. It has no privileged role in the general Psychohistory hazard and must not be used outside 
its financial assumptions merely because it is mathematically familiar.
101. OU derivation details
The OU solution over interval Δ follows by multiplying the SDE by the integrating factor exp(at). For 
mean μ, the solution is X_{t+Δ}=μ+(X_t μ)e^{-aΔ}+σ _t^{t+Δ}e^{-a(t+Δ-s)}dB_s. The stochastic integral − ∫
has zero mean and variance σ²(1 e^{-2aΔ})/(2a), yielding the exact transition density used by G2. −
E[X_{t+Δ}|X_t]=μ+(X_t−μ)e^{-aΔ}.
Var[X_{t+Δ}|X_t]=σ (1−e^{-2aΔ})/(2a). ²
As Δ grows, the conditional mean approaches μ and the variance approaches σ²/(2a). The lag correlation
of the stationary process is exp( aΔ). Recovery time 1/a, stationary variance and theoretical −
autocorrelation are therefore algebraically tied to the same fitted parameters; treating all three as 
independent signals would violate Evidence Independence.
101.1 Near-unit-root boundary
When a approaches zero, recovery time diverges and finite samples have little information separating 
weak mean reversion from a random walk. Wald intervals become unreliable because the parameter 
<PARSED TEXT FOR PAGE: 61 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
lies near a boundary and the transformation 1/a is highly nonlinear. Profile likelihood and dependence￾preserving bootstrap are therefore required.
101.2 Observation noise
Y_t=X_t+ε_t, ε_t~N(0,τ ) (candidate state-space extension). ²
Measurement noise can inflate short-lag variance and depress apparent autocorrelation. If τ² is material
and estimable, a state-space OU model should compete with the naïve OU. If τ² and σ² cannot be 
separated, recovery claims are weakened.
102. Hawkes derivation details
For a point process with conditional intensity λ(t), the likelihood on [0,T] is exp( _0^T λ(s)ds) _i λ(t_i). −∫ ∏
Taking logs yields the event-log-intensity term minus the compensator. For the exponential kernel, the 
compensator has an analytic form, which is why the exponential Hawkes model is the default 
computational benchmark.
L = exp(−∫_0^T λ(s)ds) ∏_{i=1}^N λ(t_i).
log L = Σ_i log λ(t_i) − ∫_0^T λ(s)ds.
The branching interpretation follows from the expected number of direct offspring per event, n= _0^ ∫ ∞
αe^{-βu}du=α/β. This interpretation depends on the linear Hawkes construction and cannot be 
transferred to arbitrary narrative processes.
102.1 Multivariate stability
For K event types with integrated excitation matrix A*, stationarity of the linear multivariate Hawkes 
process requires spectral radius ρ(A*)<1. Near-critical matrices produce long cascades and large 
uncertainty. Cross-excitation may be observationally confounded by common broadcasters.
102.2 Edge sparsity
High-dimensional Hawkes estimation can overfit dense excitation matrices. Candidate implementations 
may use L1/group penalties or structured priors, but penalty selection occurs inside nested validation. 
Sparsity is a regularisation choice, not proof that omitted edges do not exist.
102.3 Goodness-of-fit
Time-rescaled residuals should be uniform after exponential transformation. The framework requires 
both marginal distribution checks and serial-dependence checks. Passing a KS-style marginal test while 
residuals remain serially dependent is insufficient.
103. Jump and realised-variation appendix
For high-frequency or densely sampled narrative/market processes, realised quadratic variation 
converges under suitable semimartingale assumptions to integrated variance plus squared jumps. 
Bipower variation can estimate the continuous component under restrictive conditions.
RV_T = Σ_i r_i → ∫_0^T σ_s ds + Σ_{0<s≤T}(ΔX_s) . ² ² ²
BV_T ≈ μ_1^{-2} Σ_{i=2}^n |r_i||r_{i−1}|, μ_1=E|N(0,1)|=√(2/π).
<PARSED TEXT FOR PAGE: 62 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
The familiar π/2 scaling follows from μ_1^{-2}. Irregular sampling, market microstructure or discretised 
media counts require adapted estimators. Psychohistory records the estimator variant and assumptions 
rather than treating 'jump score' as universal.
104. Graph perturbation mathematics
104.1 Weyl
For symmetric A and perturbation E, Weyl's inequality bounds eigenvalue displacement by the spectral 
norm of E.
|λ_k(A+E)−λ_k(A)| ≤ ||E||_2.
This provides a resolution test: if the claimed change in λ2 is smaller than plausible graph-construction 
perturbation, fragmentation cannot be resolved.
104.2 Davis–Kahan
For separated invariant subspaces, the sine of the principal angle between true and perturbed 
eigenspaces is bounded by perturbation magnitude divided by an eigengap. Consequently, Fiedler￾vector direction is unreliable when λ2 and λ3 nearly coincide.
||sin Θ|| ≤ ||E||_2 / δ.
The exact δ definition follows the chosen Davis–Kahan form. Implementations store the theorem 
variant and numerical gap used.
104.3 Node-set changes
When nodes enter or leave, eigenvalue changes mix genuine topology with dimensional change. The 
default comparison uses a declared common-node panel or a graph-normalisation procedure validated 
for changing node sets. Silent node-set drift is prohibited.
105. Random-matrix appendix
For iid zero-mean observations with variance σ² and q=N/T, the Marchenko–Pastur distribution gives a 
benchmark support [σ²(1 q)², σ²(1+ q)²] when q is in the relevant regime. Financial, social and macro −√ √
panels violate iid assumptions, so this is a diagnostic reference rather than a universal null.
A BBP-style outlier transition concerns detectability of a low-rank spike against a random covariance 
bulk. Psychohistory uses the idea to ask whether a common mode is distinguishable from sampling 
noise. It does not label every separated eigenvalue a systemic transition.
RMT_NULL_SELECTION:
 if iid approximation defensible:
 MP reference permitted
 elif serial dependence material:
 use block/bootstrap or fitted time-series null
 elif heteroskedasticity/common factors known:
 preserve them in null
 if no defensible null:
 TEST_UNRESOLVED
<PARSED TEXT FOR PAGE: 63 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
106. HSIC derivation and estimator contract
Let k and l be characteristic kernels on X and Y. Population HSIC is the squared Hilbert–Schmidt norm 
of the cross-covariance operator. For finite data, Gram matrices K and L are centred with H=I 11ᵀ/n. −
HSIC_b = (1/(n−1) ) tr(KHLH) (one common biased normalisation). ²
Different libraries use slightly different finite-sample normalisations. The implementation must freeze 
one definition and unit-test it. Kernel bandwidth selection is part of the model-selection search and 
enters multiplicity/validation accounting.
106.1 Serial null
For dependent time series, cyclic shifts, block permutations or fitted surrogate processes may be 
appropriate depending on the null. The chosen null must destroy cross-dependence while retaining 
relevant marginal and temporal structure. If it destroys too much, the resulting p-value can be anti￾conservative.
107. Distance covariance appendix
Distance covariance uses pairwise Euclidean or registered metric distances. Let A and B be doubly 
centred distance matrices; sample squared distance covariance is proportional to the mean of 
elementwise products A_ijB_ij.
dCov_n (X,Y) = (1/n ) Σ_{i,j} A_ij B_ij. ² ²
Distance correlation normalises by distance variances. As with HSIC, time-series inference requires 
dependence-aware resampling. The statistic is a corroborating dependence detector, not a directional 
estimator.
108. Surrogate-generation contracts
108.1 iAAFT
Iterative amplitude-adjusted Fourier transform surrogates approximately preserve the observed 
amplitude distribution and power spectrum while randomising nonlinear phase relationships. They are
useful only when that is the nuisance structure the null should preserve.
108.2 Twin surrogates
Twin surrogates preserve aspects of recurrence structure in deterministic/nonlinear time series. They 
are candidates when ordinary phase randomisation would destroy the geometry whose presence is not 
under test.
108.3 Block bootstrap
Moving, circular or stationary block bootstrap preserves local serial dependence to a degree determined
by block length. Block length is selected by a frozen rule or inner validation, not chosen to maximise 
significance.
<PARSED TEXT FOR PAGE: 64 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
108.4 Common-driver preserving null
For candidate coupling X Y under common driver C, a custom null should preserve X–C and Y–C ↔
relationships while breaking the hypothesised direct X–Y link. Failure to construct such a null blocks 
strong coupling claims.
109. Survival-analysis appendix
109.1 Risk sets and censoring
For event time T_i and censoring C_i, observed time is min(T_i,C_i) with event indicator δ_i. Cox partial 
likelihood conditions on risk sets R_i. Independent/non-informative censoring assumptions must be 
examined; policy changes or observation dropout can violate them.
109.2 Time-varying covariates
Psychohistory features are naturally time-varying. Covariate values used for a risk interval must be 
those available at its start under the forecast contract. Future within-interval updates cannot leak into 
an earlier risk prediction.
109.3 Proportional-hazards checks
Schoenfeld-style residual diagnostics or time-interaction tests may reveal non-proportional effects. If 
violations are material, stratified, time-varying coefficient or discrete-time alternatives must compete. 
The model is not retained merely because Cox is the default.
110. Calibration uncertainty
Calibration curves are estimates and become noisy with few events. Bootstrap confidence bands should 
resample at the outcome-episode level where repeated forecasts exist. Calibration slope/intercept are 
withheld when event count is too small for stable estimation.
A perfectly calibrated but uninformative base-rate model can still have poor resolution. Psychohistory 
therefore reports calibration and proper score together rather than treating either as sufficient.
111. Decision thresholds and utility
Probability forecasts and operational warnings are separate outputs. A warning threshold requires an 
explicit utility or cost trade-off. Without one, the system reports probability and does not invent a 
universal 0.5 threshold.
Choose action a to minimise E[L(a,Y)|F_t].
Domain-specific loss may weight false alarms, missed transitions and warning lead differently. Loss 
functions are frozen before evaluating the corresponding decision policy.
112. Outcome-episode clustering
An episode is the underlying event process to which multiple forecast origins refer. Episode rules 
specify when events are considered distinct, including minimum separation and recovery/reset 
conditions. Without this, a long crisis can be counted as dozens of successes.
<PARSED TEXT FOR PAGE: 65 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
EPISODE_CLUSTER(events, contract):
 sort events by contracted start time
 merge events separated by less than minimum_separation
 apply contracted recovery/reset rule
 assign episode_id
 map forecasts to episodes by horizon overlap
113. Forecast-ledger immutability and corrections
Issued forecasts are append-only. If a source correction reveals that a forecast used erroneous input, the
original remains in the ledger with a correction link. The corrected counterfactual forecast can be 
computed for diagnosis but cannot replace the historical issued probability.
CORRECT_FORECAST_RECORD(original_id, reason):
 freeze original
 create correction_event with source evidence
 optionally compute counterfactual corrected forecast
 mark counterfactual = TRUE
 exclude counterfactual from prospective issued-forecast score
114. Evidence ancestry relation types
Relation Meaning
derives child is deterministic/statistical transform of 
parent
same_release_system observations share production pipeline
nested_geography one observation contains another geographically
shared_sample same respondents/transactions contribute
revision_of later vintage revises earlier value
semantic_descendant message descends/mutates from earlier message
common_broadcaster observations may share upstream dissemination 
source
expert_interpretation_of judgement interprets underlying observations
aggregate_contains aggregate contains subgroup
model_output_of external forecast/model derived from inputs
Ancestry edges can be uncertain. The graph stores relation confidence/notes but does not turn uncertain
provenance into a causal probability unless a separate model is defined.
115. Information breadth candidates
No universal informational-breadth scalar is admitted, but candidate research estimators can be tested. 
One simple family treats ancestry clusters as effective evidence units; another estimates effective rank 
of a whitened evidence covariance matrix. Both must be compared with leaving the evidence vector 
uncollapsed.
<PARSED TEXT FOR PAGE: 66 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
EffectiveRank(C)=exp(−Σ_i p_i log p_i), p_i=λ_i/Σ_j λ_j (candidate descriptive measure).
Effective rank is a dependence summary, not a count of causal mechanisms. It cannot replace the 
ancestry graph.
116. Source-quality and archival-survival model
Historical evidence is filtered by preservation, digitisation, language, institutional record-keeping and 
historian selection. Let S_i be the probability that an underlying event/message is observed in the 
surviving corpus. If S_i is unknown, the system records partial observation rather than assuming 
missing at random.
O_historical = Selection(M_historical;ψ) + ε.
Inverse-probability correction is permitted only if selection probabilities are estimable. Otherwise 
sensitivity analysis across plausible selection regimes is preferable to false precision.
117. Cross-era carrier model
Carrier C affects delay, reach, copying fidelity, mutation probability, broadcast capacity and topology. A 
propagation comparison across eras therefore conditions on carrier descriptors rather than simply 
rescaling clock time.
K_M(i,j,Δt | C,L,I) = reception/adoption kernel.
Candidate carrier descriptors include effective reproduction opportunity, geographic reach distribution,
copy latency, mutation/error rate and gatekeeper structure. These descriptors themselves require 
historical measurement contracts.
118. Simple versus complex contagion
Simple contagion permits adoption after a single exposure with independent per-exposure probability 
p, giving 1 (1 p)^k after k exposures. Complex contagion requires reinforcement, thresholding or − −
social confirmation.
P_simple(adopt|k)=1−(1−p)^k.
P_complex(adopt)=f(k_independent, tie_strengths, θ, context).
The selector is empirical. A narrative being politically complex does not imply complex contagion in the 
technical sense.
119. Broadcast and hybrid contagion
Broadcast processes include a source capable of exposing many nodes without traversing ordinary peer
edges. Hybrid models combine broadcast intensity b_j(t) with peer contagion. Failing to model 
broadcast can make peer networks appear artificially dense or coordinated.
λ_j(t)=b_j(t)+peer_excitation_j(t)+baseline_j(t).
<PARSED TEXT FOR PAGE: 67 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
120. Source entropy and distributed ignition
Source uncertainty may be summarised descriptively by entropy of the source posterior, U_S= Σ_s p_s −
log p_s. High entropy means source identity is uncertain; it does not prove distributed ignition.
U_S = −Σ_s P(S=s|O) log P(S=s|O).
Distributed Ignition diagnostics must compare observed spatial/network dispersion of early events with
single-source, broadcaster and observation-artifact nulls.
121. Exposure-to-response conversion
For exposure X_t and response R_{t:t+h}, candidate conversion is C_XR(t,h)=P(R_{t:t+h}|X_t,B_t), where 
B_t contains baseline predictors. The production question is incremental predictive information beyond
B_t.
ΔScore_X = Score(B+X) − Score(B).
A statistically significant exposure-response association that does not improve predictive score is not 
admitted as a forecasting feature.
122. Edge-local validation matrix
Edge class Typical null Required baseline
Narrative participation → time-preserving narrative 
surrogate
participation 
persistence/seasonality
Energy firm costs → commodity/seasonal baseline energy price alone
Firm costs output prices → sector-price baseline input-cost index
Credit property → rates/approvals baseline recognised housing leading 
indicators
Exposure network response → common-driver preserving 
graph null
node-level conventional 
predictors
Topology local stability → graph-rewired/temporal 
surrogate
G2-only model
These are templates, not automatic choices. Each experiment records the exact null and baseline.
123. State–momentum–pipeline representation
For a measured domain variable, four temporal semantics may coexist: current state S_t, momentum 
ΔS_t, pipeline Q_t and expectations E_t^subj. They are not independent merely because they are 
separate fields.
DomainTemporalVector_t=[S_t, ΔS_t, Q_t, E_t^subj].
The vector is retained until supervised evidence supports reduction. A contraction can be improving; an
expansion can be deteriorating; a pipeline can weaken while current output improves.
<PARSED TEXT FOR PAGE: 68 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
124. Shock–exposure–response representation
Shock_t → Exposure_{i,t} → Response_{i,t+h}.
Exposure is modified by dependency and buffers. A more explicit candidate form is Exposure_i,t = 
Shock_t × Dependency_i,t × (1 Buffer_i,t), but this multiplicative expression is conceptual unless scales −
support multiplication.
Buffers include hedges, inventories, savings, fixed contracts, fiscal intervention and spare capacity. 
Their presence explains why transmission can be delayed, suppressed or redirected.
125. Information-inheritance accounting
If feature z is an external forecast F_ext, or a transform of one, the minimum baseline includes F_ext 
itself. The relevant question is whether Psychohistory adds information beyond the inherited forecast.
IncrementalSkill = Skill(PH including F_ext) − Skill(F_ext or baseline containing F_ext).
This applies equally to expert expectations, mortgage approvals, new orders and any recognised leading
series.
126. Expert judgement as evidence
Expert statements can contain useful model hypotheses, but often interpret the same observations 
already present in the system. An `expert_interpretation_of` ancestry edge therefore prevents pseudo￾replication.
Expert disagreement is retained as competing hypotheses where possible. Averaging opinions into a 
consensus score can erase informative model disagreement and is not the default.
127. Geographic multiplicity
Regional, national and supranational observations can be nested. A UK aggregate plus England, 
Scotland and Wales observations do not constitute four independent replications when the aggregate 
contains the regions or methodologies differ.
Geographic search is part of multiplicity. Selecting the region with the strongest association after 
inspection is equivalent to a multiple-hypothesis search and is registered accordingly.
128. Temporal multiplicity
Testing one predictor at 1,2,…,24 month lags creates at least a lag family, and often more because 
overlapping horizons are dependent. Lag selection occurs inside nested validation; the outer holdout 
sees only the selected rule.
The same applies to smoothing windows, rolling-volatility lengths, graph aggregation windows and 
historical-anchor trajectory widths.
<PARSED TEXT FOR PAGE: 69 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
129. Hyperparameter multiplicity
Kernel bandwidths, regularisation strengths, PLS components, BOCPD priors, graph thresholds, DTW 
bands and calibration families are model-selection degrees of freedom. Nested validation accounts for 
their selection effect on predictive performance. Inferential p-values from a model chosen after broad 
tuning are not interpreted as though the model were fixed a priori.
130. Negative controls
Negative controls are variables or outcomes expected not to participate in the proposed mechanism but 
sharing important nuisance structure. They help reveal confounding and observation artefacts.
A negative control must be selected before seeing the target association. Post-hoc choice of a control that
'works' simply creates another researcher degree of freedom.
NEGATIVE_CONTROL_TEST:
 register control exposure/outcome and rationale
 verify shared nuisance structure
 run same pipeline as target hypothesis
 if control shows comparable effect:
 downgrade mechanism interpretation
131. Sensitivity analysis
Sensitivity analysis varies defensible modelling choices without searching for the most favourable 
result. Examples include observation windows, graph normalisation, reasonable prior ranges, source￾quality thresholds and alternative but predeclared outcome vintages.
A relationship that reverses under minor defensible changes is reported as fragile and cannot be 
promoted on the basis of its preferred specification.
132. Robustness versus replication
Robustness means a result persists under alternative analyses of substantially the same evidence. 
Replication means it reappears in genuinely new or sufficiently independent evidence. Multiple 
estimators on one dataset provide robustness, not replication.
This distinction is enforced by the Evidence Ancestry Graph and status ladder.
133. Power and minimum-information rules
Failure to reject a null is not evidence of absence when the test has little power. Before interpreting a 
null result, the evaluation records event count, effective sample size, resolution bound and the 
minimum effect size the design could plausibly detect.
No universal minimum sample size is specified because dependence, event rate and model dimension 
vary. Domain experiments must define simulation-based or analytic minimum-information criteria.
<PARSED TEXT FOR PAGE: 70 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
134. Class imbalance
Rare transitions create severe class imbalance. Accuracy is therefore not a primary metric. Proper 
probability scores, precision-recall summaries where useful, calibration and event-based false-alert 
accounting are preferred.
Resampling or class weighting can change probability calibration. If used for fitting, predictions must be
recalibrated and evaluated on the natural event prevalence.
135. Model drift and recalibration
A production model can degrade as observation systems and mechanisms change. Drift monitoring 
examines covariate distribution, missingness, calibration and residuals. Recalibration is a model change
and creates a new version.
DRIFT_MONITOR:
 compare current feature distribution with training reference
 check source/method versions
 check calibration on newly matured outcomes
 check residual dependence
 if drift threshold crossed:
 flag REVIEW
 do not silently retrain
136. Structural breaks in observation systems
Legal changes, survey redesigns, accounting revisions, platform API changes and diagnostic-policy 
changes can create breaks unrelated to the latent phenomenon. The observation record stores 
method_version and break flags. Cross-break models require explicit bridge studies or separate regimes.
A long historical series assembled across incompatible definitions is not automatically more informative
than a shorter consistent series.
137. Data-source hierarchy
Primary official or direct-source data are preferred for measurement. Secondary reporting is useful for 
discovery and context but does not replace the authoritative release when the underlying statistic 
matters. Conflicts are retained until resolved rather than averaged.
Commercial data may be valuable for timeliness and network structure but require coverage, selection 
and revision documentation. Proprietary opacity reduces measurement confidence even when 
predictive performance appears strong.
138. Sidecar output semantics
Signal is a concise measured state or diagnostic; Vector is the retained multidimensional representation;
Hazard is permitted only when a calibrated Outcome Contract exists. A sidecar without a calibrated 
outcome can output Signal and Vector but must leave Hazard absent rather than invent a qualitative 
risk number.
SIDE_CAR_OUTPUT:
<PARSED TEXT FOR PAGE: 71 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
 signal:
 values
 uncertainty
 status
 vector:
 feature_ids
 ancestry
 horizons
 hazard:
 probability
 outcome_contract_id
 calibration_version
 # optional; absent unless validated
139. Sidecar disagreement
Sidecars can disagree because they measure different mechanisms. Market stress can rise while real 
activity remains stable; narrative acceleration can coexist with institutional resilience. The integration 
layer retains disagreement unless a supervised model demonstrates how it predicts the contracted 
outcome.
Averaging sidecar scores is prohibited as a default because scales and meanings differ.
140. Network-of-networks candidate
A future extension may model multiplex layers for communication, finance, trade, institutions and 
participation. This is not part of admitted 2.4 production machinery. Multiplex models introduce many 
coupling parameters and are particularly vulnerable to weak identifiability.
G_multi = {G^(M),G^(E),G^(I),G^(P), interlayer edges}.
The extension may be explored only after single-layer models demonstrate predictive value.
141. Bayesian model averaging candidate
Where several well-specified models remain plausible, Bayesian or stacking-style model averaging may 
be tested. It is not used to hide disagreement. Weights are trained on predictive performance and 
cannot be set from narrative preference.
Models sharing the same evidence ancestry remain dependent; ensemble size is not evidence breadth.
142. Ensemble stacking candidate
p_stack = Σ_m w_m p_m, w_m≥0, Σ_m w_m=1.
Weights may be selected by minimising cross-validated proper score. The ensemble competes against its
best constituent and simple averaging. If stacking adds no held-out value, it is removed.
<PARSED TEXT FOR PAGE: 72 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
143. Hierarchical outcome contracts
Some domains have nested outcomes, such as local disruption, sector stress and system transition. 
These are separate contracts. A local event cannot be silently counted as a system-level success.
Hierarchical models may share information, but scoring remains at the declared outcome level.
144. Multi-horizon forecasts
Forecasts at h1,h2,… are distinct predictions. Horizon coherence is desirable but not assumed. Each 
horizon has its own baseline and calibration. Searching horizons for the best retrospective score is 
multiplicity.
Where a survival model supplies a cumulative event distribution, multi-horizon probabilities are 
derived coherently from the same fitted survival function.
145. Multi-class transitions
Some transitions are not binary. A future contract may distinguish recovery, stable continuation, 
deterioration and structural break. Multinomial or competing-risks models can be used when classes 
are operationally defined and sample size permits.
Collapsing classes into adverse/non-adverse is acceptable only if the binary contract is the actual 
decision target.
146. Competing risks
If multiple mutually exclusive event types can terminate a state, cause-specific or subdistribution 
approaches may be considered. The choice depends on whether the objective is etiological modelling or 
cumulative incidence prediction. The framework records the estimand explicitly.
147. Forecast reconciliation
Predictions across nested geographies or outcomes may be incoherent. Reconciliation is a post-model 
transform and therefore requires its own contract and held-out evaluation. Coherence alone is not 
sufficient reason to alter probabilities if it worsens proper score.
148. Interpretability
Interpretability reports feature ancestry, current values, uncertainty, baseline comparison and local 
contribution where the predictive model supports such decomposition. Post-hoc explanation methods 
are not causal explanations and are not counted as evidence.
The system should prefer direct model coefficients or transparent feature contrasts where possible, but 
predictive validity remains the primary admission criterion.
<PARSED TEXT FOR PAGE: 73 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
149. Audit report schema
AuditReport:
 run_id
 information_cutoff
 new_sources[]
 corrected_sources[]
 measurement_failures[]
 ancestry_changes[]
 new_hypotheses[]
 multiplicity_updates[]
 estimator_diagnostics[]
 coupling_tests[]
 baseline_comparisons[]
 matured_outcomes[]
 brier/logscore/calibration_if_estimable
 false_alerts_if_expired
 lead_time_if_resolved
 ablations[]
 promotions[]
 demotions[]
 specification_changes[]
 unresolved_items[]
 next_preregistered_tests[]
150. Hourly evaluation report contract
The human-facing hourly report is concise but must be generated from the full audit. It reports 
evidence, failures, changes and next priorities. Absence of a matured outcome is explicitly reported 
rather than filled with retrospective scoring.
HOURLY_REPORT:
 Evidence observed
 What it tests
 Failures / unsupported assumptions
 Multiplicity and independence status
 Model/specification changes (usually none)
 Scoring status
 Promotions/demotions
 Next frozen test
151. Storage and archival policy
Every canonical specification release is immutable and date-stamped. Later editions supersede but do 
not overwrite earlier editions. Forecast ledgers, outcome resolutions and audit reports are stored 
separately from the normative specification so empirical history cannot rewrite the rules under which 
earlier forecasts were made.
The DOCX is the editable human-readable canonical storage document for this revision; machine￾readable schemas and source code should be version-controlled separately. A PDF rendering may be 
retained as a frozen visual snapshot.
<PARSED TEXT FOR PAGE: 74 / 74>
Psychohistory 2.4 — storage edition — 6 October 2026
152. Final completeness boundary
This document defines the complete Psychohistory 2.4 architecture currently specified: mathematical 
state and observation semantics; stochastic, memetic, stability and network estimators; coupling and 
dependence tests; historical recurrence; sidecar interfaces; outcome and forecast contracts; vintage 
reconstruction; uncertainty; identifiability; multiplicity; calibration; scoring; failure states; validation; 
implementation order; APIs; storage; and falsification.
It deliberately does not invent domain-specific coefficients, empirical priors, performance statistics or 
causal parameters that have not been estimated. 'Complete' therefore means complete specification of 
the current framework, not fabricated completion of unknown empirical quantities. Unknowns remain 
explicit research variables.