#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress
from tabulate import tabulate

from collect import filter_energy_var, get_data
from plot_v_score import get_exact_energies, get_marker

out_filename = "./v_score_rel_err_heis.pdf"


def read_extra():
    exact_energy = -251.46248 / 4
    data = []
    filename = "/home/wd/anqs/data/test_scan_out_all/heis_afm_open_mars_2d_L10.txt"
    with open(filename, "r") as f:
        for line in f:
            cols = line.split()
            method = cols[0]
            energy = float(cols[2])
            energy_std = float(cols[3])

            energy_rel_err = (energy - exact_energy) / abs(exact_energy)
            v_score = 100 * energy_std**2 / energy**2

            if any(x in method for x in ["mps_rnn", "mps_qrnn", "mps_trnn"]):
                color = "C2"
            elif "mps" in method:
                color = "C3"
            elif "each" in method:
                color = "C4"
            elif "rnn" in method:
                color = "C6"
            else:
                color = "C5"

            data.append((v_score, energy_rel_err, color))
    return data


def main():
    data = get_data()
    exact_energies = get_exact_energies(data)
    data = filter_energy_var(data)

    data_new = []
    markers = []
    for row in data:
        ham_attr = row[:2]
        if ham_attr != ("Heisenberg", "square_10_OO_100"):
            continue
        exact_energy = exact_energies[ham_attr]

        _, _, method, energy, energy_var, dof, energy_inf, _ = row

        if energy < exact_energy:
            print("Warning: Lower than exact energy:", row)
            continue
        energy_rel_err = (energy - exact_energy) / abs(exact_energy)

        v_score = dof * energy_var / (energy - energy_inf) ** 2

        data_new.append((*ham_attr, method, energy_rel_err, v_score))
        markers.append(get_marker(ham_attr))
    data = data_new
    print(tabulate(data, tablefmt="plain"))

    data_new = []
    for row, marker in zip(data, markers):
        data_new.append((row[4], row[3], marker))
    data = data_new

    fig, ax = plt.subplots(figsize=(6, 4))

    for v_score, energy_rel_err, (color, marker, size) in data:
        ax.plot(
            v_score,
            energy_rel_err,
            linestyle="",
            marker=marker,
            markeredgewidth=0,
            markerfacecolor=color,
            markersize=size,
        )

    data = read_extra()
    data = sorted(data, key=lambda x: x[2])
    for v_score, energy_rel_err, color in data:
        ax.plot(
            v_score,
            energy_rel_err,
            linestyle="",
            marker="o",
            markeredgewidth=0,
            markerfacecolor=color,
            markersize=1,
            zorder=0.7,
        )

    xs = np.log([x[0] for x in data if 1e-2 < x[0] < 1])
    ys = np.log([x[1] for x in data if 1e-2 < x[0] < 1])
    lm = linregress(xs, ys)
    print(
        f"slope {lm.slope:.8g} "
        f"intercept {lm.intercept:.8g} "
        f"R-squared {lm.rvalue**2:.3g} "
        f"p-value {lm.pvalue:.3g} "
        f"slope_std_err {lm.stderr:.3g} "
        f"intercept_std_err {lm.intercept_stderr:.3g}"
    )

    def _lm(x):
        return lm.intercept + lm.slope * x

    v_min = np.log(2e-5)
    v_max = np.log(7)
    ax.plot(
        np.exp([v_min, v_max]),
        np.exp([_lm(v_min), _lm(v_max)]),
        color="k",
        linestyle="--",
        linewidth=0.5,
        zorder=0.6,
    )

    ax.set_xlabel("V-score")
    ax.set_ylabel("Energy rel. err.")
    ax.set_xlim([1.5e-5, 8.5])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(color="0.8", linestyle="--")
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")


if __name__ == "__main__":
    main()
