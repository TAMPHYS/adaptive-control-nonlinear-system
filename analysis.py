import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# -----------------------------
# GLOBAL PARAMETERS
# -----------------------------
T = 30.0
dt = 0.05
time = np.arange(0, T, dt)
P_max = 50e3
L0 = 5.0
A0 = 0.002
alpha = 0.15
gamma = 1.3
v_eff_base = 8.0
D = 1.0
NB_crit = 1.5
BURST_START = 10.0   # Strategy C burst window
BURST_END = 20.0

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# -----------------------------
# SIMULATE FUNCTION (now with Strategy C)
# -----------------------------
def simulate(strategy, L, kappa0=0.00015, stochastic=False):
    NB = 0.0
    F = 0.0
    A_eff = A0 * (L / L0)**2
    eta_atm = np.exp(-alpha * L)
    kappa_L = kappa0 * (L / L0)

    if stochastic:
        eta = np.clip(np.random.normal(0.75, 0.1), 0.5, 1.0)
        v = np.clip(np.random.normal(v_eff_base, 2.0), 5.0, 15.0)
        turb_factor = np.clip(np.random.normal(1.0, 0.15), 0.7, 1.3)
        jitter_factor = np.clip(np.random.normal(1.0, 0.10), 0.8, 1.2)
    else:
        eta = 0.75
        v = v_eff_base
        turb_factor = 1.0
        jitter_factor = 1.0

    for t in time:
        M = np.sin(np.pi * t / T)

        if strategy == "A":
            P = P_max
        elif strategy == "C":
            P = P_max if BURST_START <= t <= BURST_END else 0.0
        elif strategy == "adaptive":
            P = P_max * sigmoid(6 * M - 10 * NB)
            if NB > NB_crit:
                P = 0.0
        else:
            P = 0.0

        dNB = kappa_L * P - (v / D) * NB
        NB += dNB * dt

        S = np.exp(-gamma * NB)
        S *= np.exp(-0.5 * max(0, NB - NB_crit))
        S *= turb_factor
        jitter_degrade = 1.0 / (1.0 + jitter_factor**2)

        I = (P / (A_eff * 1e4)) * S * eta * eta_atm * jitter_degrade
        F += I * dt

    return F

# -----------------------------
# MONTE CARLO SETTINGS
# -----------------------------
N_SIM_DIST = 2000
N_SIM_K = 1000
L_test = 5.0
kappa_default = 0.00015
kappa_values = np.linspace(5e-5, 5e-4, 10)
distances = np.linspace(5, 10, 11)

# -----------------------------
# RUN ALL SIMULATIONS
# -----------------------------
# 1. Distribution @ 5 km
results_A = np.array([simulate("A", L_test, kappa0=kappa_default, stochastic=True) for _ in range(N_SIM_DIST)])
results_C = np.array([simulate("C", L_test, kappa0=kappa_default, stochastic=True) for _ in range(N_SIM_DIST)])
results_ad = np.array([simulate("adaptive", L_test, kappa0=kappa_default, stochastic=True) for _ in range(N_SIM_DIST)])

# 2. κ-sweep (mean + variance)
mean_A, mean_C, mean_ad = [], [], []
var_A, var_C, var_ad = [], [], []

for kappa in kappa_values:
    res_A = np.array([simulate("A", L_test, kappa0=kappa, stochastic=True) for _ in range(N_SIM_K)])
    res_C = np.array([simulate("C", L_test, kappa0=kappa, stochastic=True) for _ in range(N_SIM_K)])
    res_ad = np.array([simulate("adaptive", L_test, kappa0=kappa, stochastic=True) for _ in range(N_SIM_K)])
    
    mean_A.append(np.mean(res_A))
    mean_C.append(np.mean(res_C))
    mean_ad.append(np.mean(res_ad))
    var_A.append(np.var(res_A))
    var_C.append(np.var(res_C))
    var_ad.append(np.var(res_ad))

mean_A = np.array(mean_A)
mean_C = np.array(mean_C)
mean_ad = np.array(mean_ad)
var_A = np.array(var_A)
var_C = np.array(var_C)
var_ad = np.array(var_ad)

# 3. Distance sweep (deterministic)
fluence_A_dist = np.array([simulate("A", L, stochastic=False) for L in distances])
fluence_C_dist = np.array([simulate("C", L, stochastic=False) for L in distances])
fluence_ad_dist = np.array([simulate("adaptive", L, stochastic=False) for L in distances])

# -----------------------------
# PRINT RESULTS
# -----------------------------
print("=== FLUENCE DISTRIBUTION @ 5 km (N=2000) ===")
print(f"Strategy A (CW)   : {results_A.mean():.0f} ± {results_A.std():.0f} J/cm²")
print(f"Strategy C (Burst): {results_C.mean():.0f} ± {results_C.std():.0f} J/cm²")
print(f"Adaptive (Policy 4): {results_ad.mean():.0f} ± {results_ad.std():.0f} J/cm²")

print("\n=== RISK-REWARD SUMMARY (κ=0.00015) ===")
print(f"A: mean={results_A.mean():.0f}, var={results_A.var():.0f}")
print(f"C: mean={results_C.mean():.0f}, var={results_C.var():.0f}")
print(f"Ad: mean={results_ad.mean():.0f}, var={results_ad.var():.0f}")

# -----------------------------
# GENERATE & SAVE ALL PLOTS
# -----------------------------
plt.figure(figsize=(10,6))
plt.hist(results_A, bins=40, alpha=0.6, label="A (CW)")
plt.hist(results_C, bins=40, alpha=0.6, label="C (Burst)")
plt.hist(results_ad, bins=40, alpha=0.6, label="Adaptive")
plt.xlabel("Fluence (J/cm²)")
plt.ylabel("Frequency")
plt.title("Fluence Distribution @ 5 km (Fig. 5 equivalent)")
plt.legend()
plt.grid(True)
plt.savefig("fig5_distribution.png", dpi=300)

plt.figure(figsize=(10,6))
plt.plot(kappa_values, mean_A, 'b-', label="Strategy A", linewidth=2)
plt.plot(kappa_values, mean_C, 'orange', label="Strategy C", linewidth=2)
plt.plot(kappa_values, mean_ad, 'g-', label="Adaptive", linewidth=2)
plt.xlabel("Thermal Coupling κ")
plt.ylabel("Mean Fluence (J/cm²)")
plt.title("Mean Performance vs Thermal Coupling (Fig. 2)")
plt.legend()
plt.grid(True)
plt.savefig("fig2_mean_vs_kappa.png", dpi=300)

plt.figure(figsize=(10,6))
plt.plot(kappa_values, var_A, 'b-', label="Strategy A", linewidth=2)
plt.plot(kappa_values, var_C, 'orange', label="Strategy C", linewidth=2)
plt.plot(kappa_values, var_ad, 'g-', label="Adaptive", linewidth=2)
plt.xlabel("Thermal Coupling κ")
plt.ylabel("Variance of Fluence")
plt.title("Risk (Variance) vs Thermal Coupling (Fig. 3)")
plt.legend()
plt.grid(True)
plt.savefig("fig3_variance_vs_kappa.png", dpi=300)

plt.figure(figsize=(8,8))
plt.scatter(var_A, mean_A, s=80, label="A (CW)", color='blue')
plt.scatter(var_C, mean_C, s=80, label="C (Burst)", color='orange')
plt.scatter(var_ad, mean_ad, s=80, label="Adaptive", color='green')
plt.xlabel("Variance (Risk)")
plt.ylabel("Mean Fluence (Reward)")
plt.title("Risk-Reward Trade-off (Fig. 4)")
plt.legend()
plt.grid(True)
plt.savefig("fig4_risk_reward.png", dpi=300)

plt.figure(figsize=(10,6))
plt.plot(distances, fluence_A_dist, 'b-', label="Strategy A", linewidth=2)
plt.plot(distances, fluence_C_dist, 'orange', label="Strategy C", linewidth=2)
plt.plot(distances, fluence_ad_dist, 'g-', label="Adaptive", linewidth=2)
plt.xlabel("Distance (km)")
plt.ylabel("Fluence (J/cm²)")
plt.title("Fluence vs Distance (Fig. 7)")
plt.legend()
plt.grid(True)
plt.savefig("fig7_fluence_vs_distance.png", dpi=300)

print("\nAll plots successfully saved as PNG files (300 dpi).")
