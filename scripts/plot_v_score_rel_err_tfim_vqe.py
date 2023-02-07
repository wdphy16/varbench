#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate

from collect import data_key, filter_energy_var, get_data
from plot_v_score import check_exact_energy, get_exact_energies, get_v_score

out_filename = "./v_score_rel_err_tfim_vqe.pdf"


def get_padded_range(xs, pad_ratio=0.02):
    x_min = xs.min()
    x_max = xs.max()
    pad = pad_ratio * (x_max - x_min)
    v_min = x_min - pad
    v_max = x_max + pad
    return v_min, v_max


def main():
    data = get_data()
    exact_energies = get_exact_energies(data)
    data = filter_energy_var(data)
    data.sort(key=data_key)

    data_new = []
    markers = []
    for row in data:
        tag = row[7]
        if tag != "pqc":
            continue

        ham_attr = row[:2]
        ham_type, ham_param = ham_attr
        if ham_attr not in exact_energies:
            continue
        if ham_type != "TFIsing":
            continue

        if check_exact_energy(exact_energies, row):
            continue

        method = row[2]
        energy = row[3]
        exact_energy, _ = exact_energies[ham_attr]
        energy_rel_err = (energy - exact_energy) / abs(exact_energy)
        if energy_rel_err < 1e-7:
            continue

        v_score = get_v_score(row, exact_threshold=0, exact_pos=0)
        if v_score < 1e-6:
            continue

        data_new.append(
            (*ham_attr, tag, method, energy_rel_err, v_score, energy_rel_err / v_score)
        )

        if "HV" in method:
            label = "HV ansatz" if method == "VQE HV (d = 8)" else None
            color = "C0"
            marker = "+"
            size = 8
        else:
            label = "R-CX ansatz" if method == "VQE R-CX (d = 4)" else None
            color = "C1"
            marker = "x"
            size = 6
        markers.append((label, color, marker, size))
    data = data_new
    print(tabulate(data, tablefmt="plain"))

    data_new = []
    for row, marker in zip(data, markers):
        data_new.append((row[5], row[4], row[2], marker))
    data = data_new

    xs = np.log([x[0] for x in data])

    def _lm(x):
        # TODO: Update data
        return x - 1.8

    fig, ax = plt.subplots(figsize=(6 * 0.8, 4 * 0.8))

    v_min, v_max = get_padded_range(xs)
    ax.plot(
        np.exp([v_min, v_max]),
        np.exp([_lm(v_min), _lm(v_max)]),
        color="k",
        linestyle="--",
        linewidth=0.5,
        zorder=0.6,
    )

    for v_score, energy_rel_err, _, (label, color, marker, size) in data:
        ax.plot(
            v_score,
            energy_rel_err,
            label=label,
            linestyle="",
            color=color,
            marker=marker,
            markersize=size,
        )

    ax.set_xlabel("V-score")
    ax.set_ylabel("Energy rel. err.")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(color="0.8", linestyle="--", zorder=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
