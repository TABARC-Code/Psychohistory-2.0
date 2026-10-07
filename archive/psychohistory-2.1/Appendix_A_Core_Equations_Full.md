Europe/London · 10 March 2026

# A.1 Overview

This appendix formalises the mathematics behind Psychohistory 2.1, covering the R3 coupled-field model, the VHP master equation, Crossroads 3.0, and the generational sidecar hooks. It also explains discretisation, stability, calibration, and identifiability.

# A.2 R3 Core

Memetic vector dynamics: ∂M/∂t = α_M(φ_eff⊙M − M^{⊘1}) + β_M P F(N,I) − Γ_M Δ_g M − A M + C(M ⊙ (1 − B M)) + η_M ξ. Adaptive resonance: φ_eff(t)=φ₀+χΛ̃₁+κ·info_pressure+ι·policy_permission+rᵀG+d cos(θ−θ⋆). Population, resources, institutions, and geometry evolve through coupled reaction-diffusion and stress-rewiring rules.

# A.3 Crossroads 3.0

Define G1 = ||∂M/∂t||_g/(||M||+ε), G2 = σ, and G3 = dΛ₁/dt. RED is triggered only when G1>φ_eff, G2>σ_crit, and G3>0 persist for τ windows. Hysteresis and path-memory prevent threshold flicker.

# A.4 VHP

The separate formalism uses ∂t Z = −G(Z)·δF/δZ + ξ, with κ₁(t)=λ_max(H_F(Z_t)) controlling hazard through h(t)=h₀ exp(a κ₁ + b σ + c dΛ₁/dt + uᵀG + s cos(θ−θ_c)).

# A.5 Numerical notes

Use semi-implicit diffusion, operator splitting for reactions, exponential integrators on graphs, and positivity-preserving limiters. Identify parameters through sparse discovery, profile likelihoods, and rolling-origin scoring.