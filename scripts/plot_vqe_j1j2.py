#!/usr/bin/env python3

from matplotlib import pyplot as plt

energy_exact = -33.83169340557936

data = [
    (-33.8315064, 7e-3, "VQE + symmetry, 64 params", "*"),
    (-32.5094, 4.08984, "Jastrow, 512 params", "o"),
    (-33.0219, 12.9877, "RBM, α = 1, 576 params", "^"),
    (-33.690091, 1.0823506**2, "RBM, α = 8, 4384 params", "^"),
    (-33.639795, 2.0719192**2, "RBM + symmetry, α = 2, 64 params", "^"),
    (-33.807754, 1.0512438**2, "RBM + symmetry, α = 8, 256 params", "^"),
    (-32.956785, 2.1864236**2, "ARNN dense, 2 layers, 3328 params", "s"),
    (-32.23514, 0.48235652**2, "ARNN conv, 3 layers, 4 features, 292 params", "s"),
    (-32.356121, 2.8395504**2, "ARNN conv, 3 layers, 16 features, 3076 params", "s"),
    (-32.647746, 2.9224421**2, "RNN LSTM, 2 layers, 4 features, 464 params", "p"),
    (-32.654523, 2.2899139**2, "RNN LSTM, 3 layers, 16 features, 10960 params", "p"),
]

out_filename = "./vqe_j1j2.pdf"


fig, ax = plt.subplots(figsize=(12, 6))

for energy, energy_var, label, marker in data:
    energy_rel_err = (energy - energy_exact) / abs(energy_exact)
    v_score = 16 * energy_var / energy**2
    ax.scatter(v_score, energy_rel_err, label=label, marker=marker)

ax.set_title("J1-J2, 4x4")
ax.set_xlabel("V-score")
ax.set_ylabel("Energy rel. err.")
ax.set_xscale("log")
ax.set_yscale("log")
ax.grid()
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
fig.tight_layout()
fig.savefig(out_filename, bbox_inches="tight")
