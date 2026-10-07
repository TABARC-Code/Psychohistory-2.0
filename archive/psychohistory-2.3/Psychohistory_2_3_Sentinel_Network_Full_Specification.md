# Psychohistory 2.3 — Sidecar Network

Self-Contained Sentinels for Emergence, Manipulation, Inverse Inference and Predictive Conflict

Consolidated technical and academic specification

Core principle: internally maximal, externally minimal

Status: research architecture and implementation specification. Example sentinel payloads are synthetic illustrations unless explicitly linked to measured data. No claimed live calibration figures in this document should be treated as validated empirical performance.

## Executive Summary

Psychohistory 2.3 extends the coupled-field warning architecture into a network of autonomous analytical sidecars. Each sidecar consumes the complete Psychohistory state stream, remaps it into a specialist domain, detects emergent geometry, performs inverse inference over likely forcing centres, and emits only a small number of compressed observations.

The design is deliberately asymmetric between input and output. Internally, a sentinel may consume market, social, institutional, resource, topological and stochastic data at high dimensionality. Externally, it behaves like an instrument panel rather than a data warehouse: Signal, Vector, Hazard, with confidence and source trace available when useful.

The central conceptual move is to treat patterns as evidence. Coordinated changes across narratives, prices, institutions, resources and network topology may permit cautious inference about hidden forcing conditions.

The architecture distinguishes natural emergence, manipulative or externally forced coordination, phase transition, common-cause synchrony and unresolved ambiguity. It does not equate correlation with manipulation. High-confidence intent attribution requires independent evidence.

A second analytical mind — a stochastic counter-model based on Itô processes, geometric Brownian motion and option-implied information — is deliberately allowed to disagree with the behavioural/topological model. That disagreement becomes a first-class signal rather than being averaged away.

## Primary Sentinel Family

| Code | Sentinel | Primary domain | Typical compressed signals |
|---|---|---|---|
| GISC | Geopolitical Instability | State fragility, alliances, escalation | ELITE_FLOCK, RESOURCE_RIPPLE |
| CTSC | Climate Transition | Grid, minerals, migration, transition constraints | GRID_FLOCK, MINERAL_HOARD |
| TPSS | Technological Phase Shift | Compute, capability, deployment, safety | COMPUTE_FLOCK, CAPABILITY_SPRINKLER |
| BADL-M | Market Behaviour | Crowding, repricing, contagion, adoption | STEALTH_FLOCK, NARRATIVE_SPRINKLER |
| IISC | Information Integrity | Organic vs engineered propagation | MEME_FLOCK, COORDINATION_SPRINKLER |
| CCSC | Corporate Collapse | Governance, cash, audit, vendor fragility | CASH_RIPPLE, CONTROL_PHASE_SHIFT |
| SCFS | Supply Chain Fracture | Corridors, inventory, throughput, chokepoints | PORT_RIPPLE, CHOKEPOINT_SPRINKLER |

## 1. Research Position and Operating Philosophy

The system is a probabilistic early-warning and counter-risk architecture. It estimates changes in system state, transition hazard, directional pressure and source geometry. It does not claim deterministic prediction. Every high-level inference remains conditional on observables, model assumptions and graph quality.

Raw-data volume is not a measure of useful intelligence. Sidecars separate internal richness from external concision:

FULL PSYCHOHISTORY STREAM → DOMAIN REMAPPING → FEATURE CONDENSATION → PATTERN GEOMETRY → INVERSE INFERENCE → HAZARD + CONFIDENCE → SIGNAL | VECTOR | HAZARD

Competing explanations are retained. A detected synchrony is not automatically labelled manipulation. The engine maintains alternatives including common cause, organic diffusion, structural exposure, liquidity effects, coordinated activity, model misspecification and unknown.

## 2. Core Psychohistory State

All sidecars inherit a shared abstract state representation.

| Field | Meaning | Examples |
|---|---|---|
| M | Narrative / memetic state | Attention, semantic clusters, framing, symbolic compression |
| P | Participation / active population | Breadth, mobilisation, adoption, turnover, migration |
| E | Resources / constraints | Liquidity, energy, minerals, compute, affordability, logistics |
| I | Institutional throughput / robustness | Governance, enforcement, settlement, permitting, diplomacy |
| L | Topology / exposure graph | Dependencies, alliances, supply chains, ownership, propagation |

Three trigger families summarise dynamic instability: G1 for narrative or memetic acceleration, G2 for structural instability, and G3 for topology acceleration. A generic hazard layer may be represented as:

`h(t) = h0 exp(a G1 + b sigma + c d(lambda1)/dt + optional sidecar terms)`

The coefficients are calibration parameters, not universal constants.

## 3. Persistence, Hysteresis and Path Memory

Transient spikes are common. A candidate event is first observed, then tested for persistence, contradiction and decay.

OBSERVED = single-cycle anomaly; PERSISTING = survives minimum window; CONFIRMED = multiple independent channels; DECAYING = signal falling but path-memory remains; CLEARED = lower threshold crossed for sufficient time.

Hysteresis uses separate entry and exit thresholds.

## 4. Pattern Geometry Engine

Natural emergence is coherent adaptation through local coupling and distributed response. Manipulative or externally forced coordination requires stronger evidence such as non-local synchrony beyond baseline, abrupt graph rewiring, compressed timing, concentrated source geometry, or narrative spread materially outrunning structural support. Even then, the neutral label COORDINATED_ACTIVITY is preferred until intent is independently supported.

A phase-transition state is a change in governing geometry: sustained instability, rising topology acceleration, loss of previous basin stability and path-memory consistent with a new regime. Ambiguity is a valid output.

## 5. Inverse Inference

Forward: forcing node → propagation → observed field.

Inverse: observed field → candidate causes → posterior source ranking.

Methods include reverse traversal/PageRank, spectral anomaly backtrace, timing-coherence inversion, embedding-cluster source tracing, bottleneck localisation and Bayesian ranking.

## 6. Universal Output Contract

Up to three observations are emitted per cycle, ranked by hazard × salience × persistence × confidence. Required concepts are signal, vector and hazard; pattern, confidence and source trace are additional fields. Hazard and confidence remain separate.

## 7–13. Domain Sentinels

GISC maps geopolitical narratives, mobilisation, sanctions/resources, institutional throughput and alliance/logistics topology. Core signatures include ELITE_FLOCK, RESOURCE_RIPPLE, ALLIANCE_SPRINKLER and BORDER_PHASE_SHIFT.

CTSC maps climate/transition narratives, adoption/migration, minerals/water/power, permitting and grid/shipping topology. Signatures include MINERAL_HOARD, GRID_FLOCK, POLICY_RIPPLE and TRANSITION_SPRINKLER.

TPSS maps capability narratives, researcher/adoption dynamics, compute/power/fabs/data, standards/safety/export controls and technology dependencies. Signatures include COMPUTE_FLOCK, SAFETY_RIPPLE, CAPABILITY_SPRINKLER and DEPLOYMENT_PHASE_SHIFT.

BADL-M detects narrative repricing, stealth accumulation, crowding, fragility, liquidity stress and contagion. Its working market outlier formula is:

`O = (S^0.30 C^0.20 N^0.15 T^0.15 A^0.20) / (R^0.60 F^0.40)`

S = structural demand; C = capital concentration; N = narrative acceleration; T = catalyst/timing alignment; A = real-world adoption; R = composite resistance; F = fragility. Scores require normalisation and calibration and are not literal probabilities.

IISC estimates whether propagation resembles organic diffusion, common-cause synchrony or engineered amplification. Inputs include semantic reuse, cross-platform timing, graph structure, participation velocity, source diversity and observable platform integrity changes. Intent requires independent evidence.

CCSC compares executive narrative with cash generation, employee behaviour, audit/control signals, supplier dependence and market-implied stress.

SCFS tracks ports, corridors, inventory, lead times, capacity, rerouting and hidden dependency.

## 14. Stochastic Counter-Model and Predictive Conflict Layer

The independent stochastic model challenges the behavioural/topological engine. For an Itô process:

`dX = mu(X,t) dt + sigma(X,t) dB`

For geometric Brownian motion:

`d ln S = (mu - 1/2 sigma^2) dt + sigma dB`

The Black–Scholes counterpoint is:

`V_t + 1/2 sigma^2 S^2 V_SS + r S V_S - r V = 0`

## 15. Conflict as a First-Class Variable

For comparable calibrated probabilities:

`D_abs = |P_PH - P_STOCH|`

`D_signed = P_PH - P_STOCH`

Conflict classes: MODEL_CONVERGENCE, STRUCTURAL_LEAD, STOCHASTIC_WARNING, NARRATIVE_OVERSHOOT and HIDDEN_FORCE.

Never average conflict away. Preserve both estimates and their disagreement; fusion occurs at the decision layer.

## 16–18. Residual, Flock and Fusion

Stochastic residual: `epsilon_t = r_t - r_hat_stochastic,t`. Persistent coherent residuals route into inverse inference rather than automatically implying manipulation.

Flock coherence:

`C_f(t) = || sum_i v_i(t) || / sum_i ||v_i(t)||`

The cross-sidecar fusion engine detects second-order patterns, coupled chains, shared forcing centres and duplicate explanations. A generic meta-state is:

`H_meta = f(h_core, h_sidecars, D_PS, C_f, I_source)`

The fusion function must be learned or calibrated.

## 19. Bidirectional Database and Node-Mind Architecture

The database is multilayer and time-aware. Nodes may represent assets, sectors, institutions, narratives, events, resources, technologies, policies and aggregate actor classes. Edges encode dependency, influence, ownership, amplification, blocking, substitution and co-movement.

Forward traversal estimates propagation; reverse traversal estimates likely source. Each node maintains recent state, evidence provenance, confidence, contradiction history, persistence state and invalidation conditions.

## 20–22. Contracts, Configuration and Processing Loop

Each sidecar declares identity/domain, inputs from M/P/E/I/L, triggers G1/G2/G3, path memory, contradictions and raw domain signals. Processing includes field remapping, geometry detection, inverse inference, optional counter-model, persistence filtering and falsification. Output is compressed.

Master configuration enables BADL-M, GISC, CTSC, TPSS, IISC, CCSC and SCFS; preserves disagreement, suppresses duplicates and requires confidence.

Reference processing: remap → detect patterns → inverse infer → test alternatives → persistence → falsification → optional counter-model comparison → rank/compress → cross-sidecar fusion.

## 23–24. Data Quality, Contradiction, Falsification and Validation

Every material observation carries provenance, timestamp, reliability, independence estimate and decay. Copies of one underlying source are not independent confirmation. Contradictions are retained. Every high-hazard interpretation defines an invalidation condition.

Validation requires preregistered events/horizons, strictly time-ordered training/calibration/holdout, Brier score and reliability curves, lead-time and false-positive measurement, ablations, simple baselines, source-duplication/poisoning tests and publication of failures.

## 25. Governance and Safety

No individual behavioural targeting or covert personalised persuasion. Prefer aggregate actor classes and system-level nodes. Use privacy-preserving topology. Separate hazard from confidence. Mark synthetic examples. Maintain audit logs, model cards and versioned calibration. Do not present research hazard scores as investment certainty.

## 26. Synthetic Auto-Output

The specification contains a synthetic multi-sentinel payload demonstrating GISC, CTSC, TPSS, BADL-M and IISC feeding a fusion state. It is explicitly not a live-world claim.

## 27. Implementation Blueprint

Reference services: Ingestion; Evidence Ledger; Graph Store; Feature Engine; Pattern Engine; Inverse Engine; Counter-Model; Persistence Engine; Fusion Engine; Output Gateway.

Logical independence is required: a sidecar must be capable of failing, disagreeing or withholding output without forcing other sidecars into the same conclusion. Cadence is domain-calibrated and source-aware.

## 28. Academic Formulation

For sidecar k:

`Z_t^(k) = Phi_k(X_t, Y_t^(k))`

`Q_t^(k) = Psi_k(Z_t^(k), memory)`

`Source_t^(k) = arg rank_f P(f | Q_t^(k))`

`Output_t^(k) = Compress(signal, vector, hazard)`

## 29. Limitations

Hidden causes may not be identifiable; inverse problems may have multiple solutions; topology can be incomplete; social data can be manipulated; GBM/Black–Scholes are incomplete market models; disagreement may be misspecification; sidecars can become self-referential; historical backtests are vulnerable to hindsight leakage and event-definition bias; hazard and confidence must remain separate.

## 30. Development Roadmap

0 Freeze schemas and terminology. 1 Evidence ledger + graph. 2 BADL-M + IISC. 3 Stochastic counter-model. 4 GISC/CTSC/TPSS. 5 CCSC/SCFS. 6 Fusion/persistence. 7 Historical validation. 8 Shadow live operation. 9 Research release.

## 31. Final Operational Definition

A Psychohistory sidecar is a self-contained sentinel that consumes the full state stream, remaps it into a domain-specific latent field, detects visible and hidden pattern geometry, tests competing explanations, performs inverse source inference, challenges itself with independent counter-models where appropriate, and emits concise Signal-Vector-Hazard observations.

## Appendix A — Compact Symbol Glossary

M narrative/memetic field; P participation; E resources; I institutions; L topology; G1 memetic acceleration; G2/sigma structural instability; G3 topology acceleration; h(t) transition hazard; O market outlier score; S,C,N,T,A,R,F market components; D_abs/D_signed model disagreement; C_f flock coherence.

## Appendix B — Output Vocabulary

FLOCK = distributed coherent movement. RIPPLE = propagation from a disturbance. SPRINKLER = field-wide distribution implying forcing centre/topology shift. PHASE_SHIFT = persistent new operating regime. DIVERGENCE = evidence layers separating. WARNING = independent counter-model stress before structural confirmation.

## Appendix C — Research Questions

Does topology acceleration improve lead time beyond volatility baselines? Can information-integrity features reduce false manipulation classifications? When does structural lead predict stochastic confirmation rather than model error? Which sidecar pairs add incremental information after common macro factors? How stable are inverse-source rankings under missing edges/delayed observations? Does preserving disagreement outperform weighted averaging?