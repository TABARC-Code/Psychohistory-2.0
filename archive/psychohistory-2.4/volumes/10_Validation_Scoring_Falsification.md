*Outcome contracts, proper scores, calibration, false alerts, lead time and lockbox governance*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Outcome Contract
C=(event_id,domain,observable,threshold,horizon,start/end,separation,ambiguity,source,vintage,revision_policy).
No defined event and horizon means no forecast score.

# 2. Brier score
BS=(1/N)sum_i(p_i-y_i)^2.
BSS=1-BS_PH/BS_baseline.
Same sample, horizon and target vintage are required.

# 3. Log score
LogLoss=-(1/N)sum_i[y_i log p_i+(1-y_i)log(1-p_i)].

# 4. Brier decomposition
BS = Reliability - Resolution + Uncertainty (under the standard decomposition convention).
Finite-sample estimation of components requires a frozen binning/nonparametric procedure.

# 5. Calibration
calibration intercept alpha=0 and slope beta=1 are ideal under the registered calibration regression.
Report uncertainty; with too few events, mark unmeasured.

# 6. False alerts
FalseAlert = warning expires without contracted event.
Unresolved warnings are not false alerts until expiry.

# 7. Lead time
LeadTime=EventStart-FirstValidWarningTime.
IncrementalLead=Lead_PH-Lead_best_inherited_baseline.
Publication lead is not phenomenon lead.

# 8. Episode dependence
Repeated forecasts of one underlying event are clustered by episode for inferential summaries. Forecast-level scores can still be stored.

# 9. Baseline ladder
Base rate -> persistence/seasonal -> conventional domain model -> recognised leading indicator/external forecast -> minimal multivariate -> single G-family -> integrated PH.

# 10. Information inheritance
IncrementalSkill = Skill(PH including external signal)-Skill(baseline containing that signal).

# 11. Nested temporal validation
for outer future block: train = prior data minus embargo; tune transforms/lags/features/model/calibration only in inner temporal splits; freeze pipeline; predict outer block once; concatenate outer predictions as development estimate; reserve untouched lockbox for final/prospective test.

# 12. Embargo
E >= max(all effective lookbacks, including nested smoothing and feature construction).

# 13. Ablation
Delta S_j=S(M+j)-S(M).
No held-out improvement => demote/remove unless retained solely as a diagnostic with explicit non-predictive status.

# 14. Promotion gate
require measurement validity; sufficient identifiability; multiplicity control/replication where relevant; untouched/prospective incremental performance; inherited-information baseline; valid null and no leakage; else remain CANDIDATE/UNRESOLVED.

# 15. Failure criterion
The stronger Psychohistory thesis fails if additional network, anchor, sidecar and coupling structure does not improve prospective forecasts over strong conventional baselines after adequate evidence accumulation.