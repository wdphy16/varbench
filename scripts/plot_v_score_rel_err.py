#!/usr/bin/env python3

from math import sqrt

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress
from tabulate import tabulate

from collect import data_key, filter_energy_var, get_data
from plot_v_score import (
    check_exact_energy,
    get_exact_energies,
    get_legend,
    get_marker,
    get_v_score,
)

out_filename = "./v_score_rel_err.pdf"


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
        tag = row[6]
        if tag == "vafqmc":
            continue

        ham_attr = row[:2]
        if ham_attr not in exact_energies:
            continue

        if check_exact_energy(exact_energies, row):
            continue

        method = row[2]
        energy = row[3]
        exact_energy = exact_energies[ham_attr]
        energy_rel_err = (energy - exact_energy) / abs(exact_energy)
        if energy_rel_err < 1e-7:
            continue

        v_score = get_v_score(row, exact=1e-16)
        if v_score < 1e-6:
            continue

        data_new.append(
            (*ham_attr, tag, method, energy_rel_err, v_score, energy_rel_err / v_score)
        )
        markers.append(get_marker(ham_attr))
    data = data_new
    print(tabulate(data, tablefmt="plain"))

    data_new = []
    for row, marker in zip(data, markers):
        data_new.append((row[5], row[4], row[2], marker))
    data = data_new

    xs = np.log([x[0] for x in data])
    ys = np.log([x[1] for x in data])
    lm = linregress(xs, ys)
    print(
        f"slope {lm.slope:.8g} "
        f"± {lm.stderr:.3g} "
        f"intercept {lm.intercept:.8g} "
        f"± {lm.intercept_stderr:.3g} "
        f"R-squared {lm.rvalue**2:.3g} "
        f"p-value {lm.pvalue:.3g}"
    )

    # def _lm(x):
    #     return lm.slope * x + lm.intercept

    bs = ys - xs
    b_mean = bs.mean()
    b_std_err = bs.std() / sqrt(bs.size)
    ys_pred = xs + b_mean
    R_squared = (
        1 - ((ys_pred - ys) ** 2).sum() / ((ys_pred - ys_pred.mean()) ** 2).sum()
    )
    print(
        "slope = 1: "
        f"intercept {b_mean:.8g} "
        f"± {b_std_err:.3g} "
        f"R-squared {R_squared:.3g}"
    )

    def _lm(x):
        return x + b_mean

    fig, ax = plt.subplots(figsize=(6, 4))

    v_min, v_max = get_padded_range(xs)
    ax.plot(
        np.exp([v_min, v_max]),
        np.exp([_lm(v_min), _lm(v_max)]),
        color="k",
        linestyle="--",
        linewidth=0.5,
        zorder=0.6,
    )

    for v_score, energy_rel_err, tag, (color, marker, size) in data:
        if tag == "vqe":
            ax.plot(
                v_score,
                energy_rel_err,
                linestyle="",
                marker=marker,
                markeredgecolor=color,
                markeredgewidth=1,
                markerfacecolor=color,
                markersize=size,
            )
        else:
            ax.plot(
                v_score,
                energy_rel_err,
                linestyle="",
                marker=marker,
                markeredgewidth=0,
                markerfacecolor=color,
                markersize=size,
            )

    ax.set_xlabel("V-score")
    ax.set_ylabel("Energy rel. err.")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(color="0.8", linestyle="--", zorder=0.4)
    ax.legend(handles=get_legend(skip=("square_kagome",)), ncol=2, columnspacing=1)
    fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")


if __name__ == "__main__":
    main()
