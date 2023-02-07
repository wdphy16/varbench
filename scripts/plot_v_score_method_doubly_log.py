#!/usr/bin/env python3

from matplotlib import pyplot as plt
from tabulate import tabulate

from collect import data_key, filter_energy_var, get_data
from plot_v_score import get_exact_energies, get_v_score, ham_colors
from plot_v_score_doubly_log import scale_doubly_log
from plot_v_score_ham import get_lattice, lat_types
from plot_v_score_method import show_tag

out_filename = "./v_score_method_doubly_log.pdf"

known_tags = ["mps", "vmc", "nqs", "pqc"]

v_score_exact_threshold = 1e-12
v_score_exact_pos = 1e-16


def main():
    data = get_data()
    exact_energies = get_exact_energies(data)
    data = filter_energy_var(data)
    data.sort(key=data_key)

    data_chain = []
    data_j1j2 = []
    data_tmp = []
    for row in data:
        ham_attr = row[:2]
        if (
            row[0] == "J1J2"
            # and row[7] != "pqc"
            and ham_attr in exact_energies
            and exact_energies[ham_attr][1] == "ed"
        ):
            continue

        # size = int(row[5])
        # if size <= 16:
        #     continue

        tag = row[7]
        if tag == "exact_qmc":
            continue
        if tag in ["rbm", "rnn"]:
            tag = "nqs"

        lattice = get_lattice(ham_attr)
        if lattice == "rectangular":
            lattice = "square"

        v_score = get_v_score(row, v_score_exact_threshold, v_score_exact_pos)

        if lattice == "chain":
            data_chain.append((row[0], (tag, lattice), v_score))
        elif lattice == "diagonal":
            data_j1j2.append((row[0], (tag, lattice), v_score))
            data_tmp.append(row + (v_score,))
    del data
    print(tabulate(data_tmp, tablefmt="plain"))

    fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(6 * 0.8, 4 * 0.8))

    for ax, data in zip(axes, (data_chain, data_j1j2)):
        tag_lats = sorted(
            {x[1] for x in data},
            key=lambda x: (-known_tags.index(x[0]), list(lat_types).index(x[1])),
        )

        xs = []
        ys = []
        cs = []
        for ham_type, tag_lat, v_score in data:
            xs.append(v_score)
            ys.append(tag_lats.index(tag_lat))
            cs.append(ham_colors[ham_type])

        for x, y, c in zip(xs, ys, cs):
            ax.scatter(
                scale_doubly_log(x), y, edgecolor=c, facecolor="none", linewidth=0.5
            )

        y_max = len(tag_lats)
        for i in range(y_max // 2 + 1):
            ax.axhspan(i * 2 - 0.5, i * 2 + 0.5, color="0.95", zorder=0.3)

        ax.set_ylim(-1, y_max)

        ax.set_yticks(range(y_max))
        ax.set_yticklabels([show_tag(x, 0) for x in tag_lats], fontsize="small")
        ax.yaxis.set_tick_params(length=0)

        ax.grid(axis="x", color="0.8", linestyle="--")
        ax.set_axisbelow(True)

        # ax_symb = ax.twinx()
        # ax_symb.spines.left.set_position(("outward", 2))
        # ax_symb.spines.left.set_visible(False)
        # ax_symb.spines.right.set_visible(False)
        # ax_symb.spines.top.set_visible(False)
        # ax_symb.spines.bottom.set_visible(False)
        # ax_symb.yaxis.set_ticks_position("left")
        # ax_symb.yaxis.set_tick_params(length=0)
        # ax_symb.set_ylim(-1, y_max)
        # ax_symb.set_yticks(range(y_max))
        # ax_symb.set_yticklabels(
        #     [lat_types[x[1]] for x in tag_lats],
        #     font="VarbenchIcons",
        #     fontsize="small",
        # )

    ax = axes[1]
    ax.set_xlabel("V-score")
    ax.set_xlim(-4.2, 0.2)
    ax.set_xticks([-4, -3, -2, -1, 0])
    ax.set_xticklabels(
        [
            "$< 10^{-16}$",
            "$10^{-8}$",
            "$10^{-4}$",
            "$10^{-2}$",
            "$10^{-1}$",
            # "$10^{-0.5}$",
        ]
    )

    axes[0].text(0.05, 0.15, "(A) 1D chains", transform=axes[0].transAxes)
    axes[1].text(0.05, 0.15, "(B) 2D $J_1$-$J_2$", transform=axes[1].transAxes)

    fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")


if __name__ == "__main__":
    main()
