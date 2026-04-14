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

### Adaptive Policy (Policy 4)
- State-dependent feedback policy  
- Modulates input based on:
  - thermal state (N_B)  
  - geometric opportunity  
- Avoids negative gain regime  
- Balances immediate reward vs future cost  

---

## Results

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

- `model.py`  
  Core simulation model and system dynamics  

- `analysis.py`  
  Generates all plots:
  - fluence distribution  
  - distance scaling  
  - performance ratio  
  - κ sweep  

---

## How to Run


python analysis.py
# <img width="859" height="547" alt="image" src="https://github.com/user-attachments/assets/8406fff3-d1d4-4ef4-894a-e437992a8645" />

 #   <img width="850" height="547" alt="image" src="https://github.com/user-attachments/assets/f37822d3-9655-4723-83fe-7ad9e569baef" />

# <img width="859" height="547" alt="image" src="https://github.com/user-attachments/assets/0da0ab8f-daaf-438c-bbe3-3185f4517758" />

# <img width="833" height="547" alt="image" src="https://github.com/user-attachments/assets/0b907e42-67cd-4f0b-9727-0c19bfae27a8" />
