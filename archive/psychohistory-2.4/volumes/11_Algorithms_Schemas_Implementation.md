*Executable pseudocode, database contracts, APIs, tests and reproducibility*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Core database
observations: id, variable, reference interval, publication, availability, vintage, value, units, method
sources: id, identifier, authority, retrieval, method version
ancestry_edges: parent, child, relation, confidence
feature_contracts: id, parents, transform, role, lookback, uncertainty
hypotheses: id, family, variables, lags, null, multiplicity, status
outcome_contracts: event, horizon, source, vintage, ambiguity, expiry
forecasts: issue time, probability, model hash, contract, baselines, vintages
outcomes: contract, episode, value, vintage, resolution time
anchors: id, pre-outcome representation, uncertainty, class
models: hash, training range, config, status
evaluation_runs: manifest, metrics, failures, changes

# 2. API contracts
ObservationProvider.snapshot(cutoff)->ObservationSet
MeasurementValidator.validate(O)->ValidatedO
AncestryGraph.update(O)->EvidenceGraph
FeatureOperator.transform(O,cutoff,state)->FeatureBundle
AnchorEngine.retrieve(state,cutoff)->AnchorBundle
Predictor.predict(features,contract)->RawRisk
Calibrator.transform(raw)->Probability
Ledger.issue(record)->immutable ForecastID
OutcomeResolver.resolve(contract,now)->Outcome|UNRESOLVED
Scorer.score(...)->MetricBundle

# 3. Canonical loop
INITIALISE registries/contracts/hashes
AT t:
snapshot point-in-time data
validate measurement and ancestry
run G1,G2,G3 and conditional G23
run dependence/sequential detectors
run enabled sidecars
assemble vector state
retrieve anchors and counter-anchors
apply admission gates
issue immutable forecasts + baselines
resolve only newly mature outcomes
score only forecasts issued before outcomes
audit leakage/redundancy/identifiability/multiplicity/revisions
write manifest

# 4. Run manifest
run_id; timestamp; code_commit; environment_lock_hash; random_seeds; source_vintage_manifest; observation_schema_version; outcome_contract_versions; hypothesis_registry_hash; feature_contract_hash; model_hash; calibration_hash; baseline_hashes; output_hashes.

# 5. Unit tests
- later revisions absent from historical snapshots
- deterministic transforms do not increase evidence breadth
- OU simulated recovery
- Poisson null does not systematically create Hawkes excitation
- graph relabelling invariance
- Fiedler sign invariance
- common-driver surrogate blocks pseudo-coupling
- forecast records immutable
- embargo covers nested lookbacks
- calibrator uses cross-fitted predictions
- anchor excludes post-outcome data
- all searched lags/horizons registered
- not-yet-released missingness preserved

# 6. Failure-state enum
VALID, EXPLORATORY_ONLY, WEAKLY_IDENTIFIED, PROCESS_UNRESOLVED, SOURCE_UNRESOLVED, TEST_UNRESOLVED, REVISION_UNSTABLE, ANCESTRY_REDUNDANT, HORIZON_UNRESOLVED, OUTCOME_UNRESOLVED, DEVELOPMENT_EXPOSED, ADMITTED.

# 7. Build order
01 vintage store
02 observations/sources
03 ancestry graph
04 outcome contracts/ledger
05 baseline library
06 scoring/episode resolver
07 G2
08 G1
09 G3
10 surrogates/dependence
11 BOCPD
12 Stage A
13 Stage B/calibration
14 anchor kNN baseline
15 uncertainty-aware anchors
16 sidecars one-by-one
17 G23 after G2/G3 validation
18 prospective issuance
19 lockbox
20 evaluate/ablate/delete

# 8. Storage
Specification releases and forecast ledgers are immutable/versioned separately. A later model may supersede but never rewrite the information state under which an earlier forecast was issued.