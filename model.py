import numpy as np

# -----------------------------
# GLOBAL PARAMETERS
# -----------------------------
T = 30
dt = 0.01
time = np.arange(0, T, dt)

P_max = 50e3
eta_overlap = 0.75

L0 = 5
A0 = 0.002

alpha = 0.15

gamma = 1.3
v_eff = 8
D = 1.0

NB_crit = 1.5

# -----------------------------
# HELPERS
# -----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# -----------------------------
# CORE SIMULATION
# -----------------------------
def simulate(strategy, L, kappa0=0.00015, stochastic=False):
    NB = 0
    F = 0

    A_eff = A0 * (L / L0)**2
    eta_atm = np.exp(-alpha * L)
    kappa_L = kappa0 * (L / L0)

    if stochastic:
        eta = np.clip(np.random.normal(0.75, 0.1), 0.5, 1.0)
        v = np.clip(np.random.normal(v_eff, 2), 5, 15)
    else:
        eta = eta_overlap
        v = v_eff

    NB_traj = []

    for t in time:
        M = np.sin(np.pi * t / T)

        if strategy == "A":
            P = P_max

        elif strategy == "adaptive":
            P = P_max * sigmoid(6*M - 10*NB)
            if NB > NB_crit:
                P = 0

        dNB = kappa_L * P - (v / D) * NB
        NB += dNB * dt

        # Smooth nonlinear loss (FINAL version)
        S = np.exp(-gamma * NB)
        S *= np.exp(-0.5 * max(0, NB - NB_crit))

        I = (P / (A_eff * 1e4)) * S * eta * eta_atm
        F += I * dt

        NB_traj.append(NB)

    return F, np.array(NB_traj)