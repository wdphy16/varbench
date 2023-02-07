#!/usr/bin/env python3

from matplotlib import pyplot as plt
from tabulate import tabulate

from collect import data_key, filter_energy_var, get_data
from plot_v_score import (
    check_exact_energy,
    get_exact_energies,
    get_exact_marker,
    get_legend,
    get_marker,
    get_plot_kwargs,
    get_v_score,
    ham_colors,
    scale_doubly_log,
    sort_v_scores,
)

out_filename = "./v_score_doubly_log.pdf"

v_score_exact_threshold = 1e-12
v_score_exact_pos = 1e-16


def main():
    data = get_data()
    exact_energies = get_exact_energies(data)
    data = filter_energy_var(data)
    data.sort(key=data_key)

    v_scores = {}
    energies = {}
    data_new = []
    markers = []
    for row in data:
        if check_exact_energy(exact_energies, row):
            continue

        ham_attr = row[:2]
        energy = row[3]
        v_score = get_v_score(row, v_score_exact_threshold, v_score_exact_pos)
        if ham_attr not in v_scores or energy < energies[ham_attr]:
            v_scores[ham_attr] = v_score
            energies[ham_attr] = energy

        method = row[2]
        data_new.append((*ham_attr, method, v_score))
        markers.append(get_marker(ham_attr))
    data = data_new
    print(tabulate(data, tablefmt="plain"))

    ham_idxs, idx_hams = sort_v_scores(v_scores)
    x_max = len(ham_idxs)

    fig, ax = plt.subplots(figsize=(21, 9))

    for (ham_type, ham_param, _, v_score), (color, marker, size) in zip(data, markers):
        ham_attr = ham_type, ham_param
        idx = ham_idxs[ham_attr]
        ax.plot(
            idx,
            scale_doubly_log(v_score),
            **get_plot_kwargs(
                color, marker, size, bold=(v_score == v_scores[ham_attr])
            ),
        )

    for i in range(x_max // 2 + 1):
        ax.axvspan(i * 2 - 0.5, i * 2 + 0.5, color="0.95", zorder=0.3)

    ax.set_ylabel("V-score")
    ax.set_xlim([-1, x_max])
    ax.set_ylim(-4.2, 1.3)
    ax.set_yticks([-4, -3, -2, -1, 0, 1])
    ax.set_yticklabels(
        [
            "$< 10^{-16}$",
            "$10^{-8}$",
            "$10^{-4}$",
            "$10^{-2}$",
            "$10^{-1}$",
            "$10^{-0.5}$",
        ]
    )

    ax.set_xticks(range(x_max))
    ax.xaxis.tick_top()
    ax.xaxis.set_tick_params(length=0)
    ax.set_xticklabels(
        [get_exact_marker(exact_energies, idx_hams[i]) for i in range(x_max)],
        fontfamily=["monospace", "VarbenchIcons"],
        rotation=90,
    )
    for i, text in enumerate(ax.get_xticklabels()):
        text.set_color(ham_colors[idx_hams[i][0]])

    ax.grid(axis="y", color="0.8", linestyle="--", zorder=0.4)
    ax.legend(
        handles=get_legend(),
        ncol=2,
        fontsize="xx-large",
        # markerscale=2,
        handlelength=1,
        columnspacing=1,
    )
    fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")


if __name__ == "__main__":
    main()
