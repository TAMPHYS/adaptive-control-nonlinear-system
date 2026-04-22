# Adaptive Control under Nonlinear Feedback and Uncertainty

## Overview

This project studies optimal decision-making in a nonlinear dynamical system where continuous input becomes counterproductive due to state-dependent feedback. The motivating example is high-energy laser propagation through the atmosphere, where thermal blooming introduces a path-dependent degradation effect.

The core question is:

> *When is it optimal to act continuously, and when should action be suppressed due to future cost?*

This is formulated as a **stochastic optimal control problem** and solved using a state-dependent adaptive policy.

---

## Key Insight

In linear systems, increasing input monotonically increases output.  
In this system, however:

- Applying more power increases immediate output  
- But also **degrades future performance** via thermal buildup  

This leads to a **negative gain regime**, where:

> Increasing input **reduces** effective output

The optimal strategy is therefore **not continuous maximization**, but **state-aware control**.

---

## Model

### State Dynamics

The system evolves according to:

dN_B/dt = κ P(t) − (v / D) N_B(t)

where:

- N_B(t): thermal distortion (path-dependent state)  
- κ: thermal coupling coefficient  
- v: effective clearing velocity  
- D: aperture scale  

---

### Output (Fluence)

Total delivered energy is:

F = ∫ I(t) dt

with:

- geometric spreading ∝ 1 / L²  
- atmospheric attenuation ∝ exp(−αL)  
- nonlinear loss ∝ exp(−γ N_B)

---

### Objective

The system is evaluated using a risk-adjusted objective:

maximize:  E[F] − λ Var(F)

This captures both:
- performance (expected fluence)  
- robustness (variance under uncertainty)

---

## Strategies Compared

### Strategy A — Continuous Wave (CW)
- Constant maximum input  
- Ignores system state  
- Efficient in linear regimes  
- Fails under strong nonlinear feedback  

---
### Strategy C: (peak burst)
- The Optimal Phased Playbook (Probe → Strike → Pulse). 
- three-stage temporal phasing policy.
- synchronize maximum power delivery with the peak geometric advantage of the zenith window while proactively
  managing the atmospheric thermal clearing time.
  
  ---
### Adaptive Policy (Policy 4)
- State-dependent feedback policy  
- Modulates input based on:
  - thermal state (N_B)  
  - geometric opportunity  
- Avoids negative gain regime  
- Balances immediate reward vs future cost  

---


# Full Details of the Simulation (Summary)
Model Type

Discrete-time Euler integration of thermal blooming ODE with adaptive bang-bang-like policy.
Time horizon: 5 s (drone engagement window).
Timestep: dt = 0.01 s (600 steps).

Fixed (Deterministic) Parameters

P_max = 50 000 W
L0 = 5 km (reference range)
A0 = 0.002 m² (reference area)
Atmospheric attenuation: α = 0.15 km⁻¹
Strehl exponent: γ = 1.3
Clearing velocity base: v_eff = 8 m/s
Aperture: D = 1.0 m (simplified)
Critical blooming: NB_crit = 1.5
Geometric modulation: M(t) = sin(π t / T) (zenith window effect)

Stochastic Variables (only when stochastic=True) — 4 independent sources

Overlap efficiency (η): Normal(μ = 0.75, σ = 0.1), clipped [0.5, 1.0]
Clearing velocity (v): Normal(μ = 8.0, σ = 2.0), clipped [5, 15] m/s
Turbulence factor: Normal(μ = 1.0, σ = 0.15), clipped [0.7, 1.3] (multiplies Strehl)
Jitter factor: Normal(μ = 1.0, σ = 0.10), clipped [0.8, 1.2] (quadratic spot-size penalty)

Monte Carlo Settings

Random seed: 42 (fully reproducible)
Distribution plot (Fig. 5 equivalent): N_SIM = 2000 realizations per strategy
κ-sweep (Fig. 2 & 3 equivalent): N_SIM = 1000 per κ value (10 κ points)
Distance sweep (Fig. 7 equivalent): deterministic (stochastic=False)

Results from this exact run
Distribution @ 5 km (κ₀ = 0.00015, N=2000)

Strategy A (CW): 3861 ± 1396 J/cm² (CV = 36.2%)
Adaptive (Policy 4): 3315 ± 996 J/cm² (CV = 30.0%)
Variance ratio (Adaptive / A) = 0.509 (≈49% lower variance)

### 1. Distribution (5 km)
- Continuous strategy: higher mean, higher variance  
- Adaptive strategy: lower variance, more robust  

---

### 2. Distance Scaling
- At short range: continuous strategy performs well  
- At longer range: nonlinear effects dominate  
- Adaptive policy **outperforms** due to controlled input  

---

### 3. Regime Transition
A clear crossover is observed:

- Linear regime → continuous optimal  
- Nonlinear regime → adaptive optimal  

---

### 4. Thermal Coupling (κ) Sweep
- Increasing κ strengthens nonlinear effects  
- Adaptive policy becomes increasingly superior  

---

## Interpretation

The results demonstrate that:

- Optimal strategies depend on system regime  
- Continuous maximization is suboptimal under feedback  
- Adaptive control improves **risk-adjusted performance**
  

---

## Code Structure

- `analysis.py`
-  Core simulation model and system dynamics  
  Generates all plots:
  - fluence distribution  
  - distance scaling  
  - risk vs coupling  
  - κ sweep  

---


# <img width="859" height="547" alt="image" src="https://github.com/user-attachments/assets/a28f38a7-64be-475a-b0bf-f47637e1d6cb" />


 #   <img width="859" height="547" alt="image" src="https://github.com/user-attachments/assets/7769f1bb-1b15-4b25-a569-7c36e947aa0d" />


# <img width="846" height="547" alt="image" src="https://github.com/user-attachments/assets/50d5b4d8-aa8b-48fd-b594-889a809e76ec" />


# <img width="859" height="547" alt="image" src="https://github.com/user-attachments/assets/48f105a4-25a0-40a2-bb7c-253e0ca9f715" />

