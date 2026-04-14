import numpy as np
import matplotlib.pyplot as plt
from model import simulate

# -----------------------------
# SETTINGS
# -----------------------------
N_SIM = 200
L_test = 5

# -----------------------------
# 1. DISTRIBUTION @ 5 km
# -----------------------------
results_A = []
results_ad = []

for _ in range(N_SIM):
    F_A, _ = simulate("A", L_test, stochastic=True)
    F_ad, _ = simulate("adaptive", L_test, stochastic=True)

    results_A.append(F_A)
    results_ad.append(F_ad)

results_A = np.array(results_A)
results_ad = np.array(results_ad)

plt.figure()
plt.hist(results_A, bins=30, alpha=0.5, label="A")
plt.hist(results_ad, bins=30, alpha=0.5, label="Adaptive")
plt.xlabel("Fluence (J/cm²)")
plt.ylabel("Frequency")
plt.title("Fluence Distribution @ 5 km")
plt.legend()
plt.show()

# -----------------------------
# 2. DISTANCE SWEEP
# -----------------------------
distances = np.linspace(5, 10, 20)

fluence_A = []
fluence_ad = []

for L in distances:
    F_A, _ = simulate("A", L)
    F_ad, _ = simulate("adaptive", L)

    fluence_A.append(F_A)
    fluence_ad.append(F_ad)

fluence_A = np.array(fluence_A)
fluence_ad = np.array(fluence_ad)

plt.figure()
plt.plot(distances, fluence_A, label="Strategy A", linewidth=2)
plt.plot(distances, fluence_ad, label="Adaptive", linewidth=2)
plt.xlabel("Distance (km)")
plt.ylabel("Fluence (J/cm²)")
plt.title("Fluence vs Distance")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 3. RATIO PLOT
# -----------------------------
ratio = fluence_ad / fluence_A

plt.figure()
plt.plot(distances, ratio, linewidth=2)
plt.axhline(1, linestyle='--')
plt.xlabel("Distance (km)")
plt.ylabel("Adaptive / A")
plt.title("Performance Ratio")
plt.grid()
plt.show()

# -----------------------------
# 4. κ SWEEP
# -----------------------------
kappa_values = np.linspace(5e-5, 5e-4, 10)

mean_A = []
mean_ad = []

for kappa in kappa_values:
    results_A = []
    results_ad = []

    for _ in range(N_SIM):
        F_A, _ = simulate("A", L_test, kappa0=kappa, stochastic=True)
        F_ad, _ = simulate("adaptive", L_test, kappa0=kappa, stochastic=True)

        results_A.append(F_A)
        results_ad.append(F_ad)

    mean_A.append(np.mean(results_A))
    mean_ad.append(np.mean(results_ad))

plt.figure()
plt.plot(kappa_values, mean_A, label="A", linewidth=2)
plt.plot(kappa_values, mean_ad, label="Adaptive", linewidth=2)
plt.xlabel("Thermal Coupling (κ)")
plt.ylabel("Mean Fluence")
plt.title("Performance vs κ")
plt.legend()
plt.grid()
plt.show()