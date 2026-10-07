*Observation models, revisions, ancestry, missingness and real-time reconstruction*

Psychohistory 2.4 | Canonical storage revision | 6 October 2026

# 1. Observation record
o_i=(value,units,scale,reference_start,reference_end,publication_time,availability_time,vintage,method_version,source_id).

# 2. General measurement equation
O_i = g_i(X_{r_i}, C_i, Q_i;theta_i) + epsilon_i.
Administrative, survey, transaction, media and sensor observations require different g_i. Identity observation is a declared special case.

# 3. Real-time vintage reconstruction
x^RT_{j,s|t}=x_{j,s}^{(max{v: availability(v)<=t})}.
Revision_{j,s}^{v*,t}=x_{j,s}^{(v*)}-x^RT_{j,s|t}.
RECONSTRUCT(cutoff): select latest vintage available by cutoff; preserve missing-at-cutoff values; preserve method version in force; prohibit later backfill; emit panel + vintage manifest.

# 4. Information maturity
A release can be timely but incomplete. Completeness fraction, sample maturity or reporting coverage is stored separately from vintage number. Later maturation of the same observation is not independent confirmation.

# 5. Composition and substitution
Delta Aggregate = WithinGroup + Composition + Substitution + Residual.
This is an accounting framework. Exact decomposition requires known weights and group definitions.

# 6. Evidence ancestry graph
T_E=(V_E,E_E,R_E), where R_E labels derives/shared_sample/nested_geography/revision/common_broadcaster/etc.
Breadth_informational <= Breadth_observed.

# 7. Transform ancestry
z_k=f(z_1,...,z_m) deterministic => evidence_rank(z_1,...,z_m,z_k) <= evidence_rank(z_1,...,z_m).
MoM, YoY, z-score and deviations of one series are representations, not independent votes.

# 8. Missingness
M_i in {structural,not_released,outage,suppressed,not_applicable,unknown}.
Imputation is fitted using past information only and carries an indicator/uncertainty. Future backfill is leakage.

# 9. Observation-process breaks
Legal changes, survey redesign, diagnostic policy, API changes and corrections create structural breaks. Bridge models require explicit evidence; otherwise regimes remain separate.

# 10. Archival selection
O_historical = Selection(M_historical;psi) + epsilon.
Historical survival is not missing-at-random by default. Sensitivity analysis is preferred when selection probabilities are not estimable.

# 11. Measurement gate
VALIDATE(o): verify source/timestamp; units/scale; reference interval/revision; composition/sample/method; uncertainty/defects; identifiability; route VALID / EXPLORATORY_ONLY / EXCLUDE.