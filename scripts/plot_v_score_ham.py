#!/usr/bin/env python3

import re
from math import gcd, log10

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

from collect import data_key, filter_energy_var, get_data, ham_types
from plot_v_score import (
    check_exact_energy,
    get_exact_energies,
    get_lattice,
    get_v_score,
    ham_colors,
)

out_filename = "./v_score_ham.pdf"

lat_types = {
    "chain": "\x01",
    "rectangular": "\x02",
    "square": "\x02",
    "triangular": "\x03",
    "diagonal": "\x07",
    "kagome": "\x04",
    "shuriken": "\x05",
    "pyrochlore": "\x06",
    "impurity": "\x08",
}

v_score_exact_threshold = 1e-12
v_score_exact_pos = 1e-15


def get_aspect(ham_param):
    if ham_param.startswith("square_"):
        return 1, 1

    match = re.compile(r"-(\d+)x(\d+)_").search(ham_param)
    if not match:
        raise ValueError(f"Failed to parse aspect ratio: {ham_param}")

    x = int(match.group(1))
    y = int(match.group(2))
    if x > y:
        x, y = y, x
    d = gcd(x, y)
    x //= d
    y //= d
    return x, y


def get_boundaries(ham_attr):
    ham_type, ham_param = ham_attr
    if ham_type == "Impurity":
        return "  "

    match = re.compile(r"_([AOP]+)").search(ham_param)
    if not match:
        raise ValueError(f"Failed to parse boundaries: {ham_param}")
    s = match.group(1)

    s = "".join(sorted(s, reverse=True))
    if all(c == s[0] for c in s):
        s = s[0] + " "

    return s


def get_extra_param(ham_param):
    match = re.compile(r"_([-.\d]+(_t12)?(_UV1V2)?)$").search(ham_param)
    if not match:
        raise ValueError(f"Failed to parse Hubbard U: {ham_param}")
    U = match.group(1)
    return U


def get_key(row):
    ham_type, ham_param, _, _, _, dof, _, _ = row
    lattice = get_lattice((ham_type, ham_param))
    if lattice in ["rectangular", "diagonal"]:
        aspect = get_aspect(ham_param)
    else:
        aspect = (1, 1)
    boundaries = get_boundaries((ham_type, ham_param))
    if ham_type in ["TFIsing", "J1J2", "tV", "Hubbard"]:
        extra_param = get_extra_param(ham_param)
    else:
        extra_param = ""
    return (ham_type, lattice, aspect, boundaries), (dof, extra_param)


def ham_attr_key(ham_attr):
    ham_type, lattice, aspect, boundaries = ham_attr
    return (
        ham_types.index(ham_type),
        list(lat_types).index(lattice),
        aspect[0] / aspect[1],
        ["  ", "O ", "PO", "P ", "PA"].index(boundaries),
    )


def get_ax_left_yticks(ham_attrs):
    last_i = 0
    last_ham_type = None
    yticks = []
    for i, ham_attr in enumerate(ham_attrs):
        ham_type = ham_attr[0]
        if last_ham_type is None:
            last_ham_type = ham_type
        if ham_type != last_ham_type:
            yticks.append((last_i + i - 1) / 2)
            last_i = i
            last_ham_type = ham_type
    yticks.append((last_i + i) / 2)
    return yticks


def show_ham_attr(ham_attr):
    _, lattice, aspect, boundaries = ham_attr
    if aspect != (1, 1):
        aspect = f"{aspect[0]}:{aspect[1]}"
        # aspect = aspect.replace("1:8", "⅛")
        # aspect = aspect.replace("1:4", "¼")
        # aspect = aspect.replace("1:2", "½")
        # aspect = aspect.replace("7:8", "⅞")
        return f"{aspect}  {boundaries}"
    return f"{boundaries}"


def main():
    data = get_data()
    exact_energies = get_exact_energies(data)
    data = filter_energy_var(data)
    data.sort(key=data_key)

    v_scores = {}
    energies = {}
    for row in data:
        if check_exact_energy(exact_energies, row):
            continue

        energy = row[3]
        key = get_key(row)
        v_score = get_v_score(row, v_score_exact_threshold, v_score_exact_pos)

        if key not in v_scores or energy < energies[key]:
            v_scores[key] = v_score
            energies[key] = energy

    ham_attrs = sorted({x[0] for x in v_scores}, key=ham_attr_key)

    xs = []
    ys = []
    cs = []
    for (ham_attr, _), v_score in v_scores.items():
        xs.append(v_score)
        ys.append(ham_attrs.index(ham_attr))
        cs.append(ham_colors[ham_attr[0]])

    fig = plt.figure(figsize=(6, 4))
    xlim1 = (1e-16, 6.5e-4)
    xlim2 = (1.5e-4, 1.5e-1)
    gs = GridSpec(
        1,
        2,
        wspace=0.02,
        width_ratios=[log10(xlim1[1] / xlim1[0]), log10(xlim2[1] / xlim2[0]) * 12],
    )
    ax = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    for x, y, c in zip(xs, ys, cs):
        if x < xlim2[0]:
            ax.scatter(x, y, edgecolor=c, facecolor="none", linewidth=0.5)
        else:
            ax2.scatter(x, y, edgecolor=c, facecolor="none", linewidth=0.5)

    y_max = len(ham_attrs)
    for i in range(y_max // 2 + 1):
        ax.axhspan(i * 2 - 0.5, i * 2 + 0.5, color="0.95", zorder=0.3)
        ax2.axhspan(i * 2 - 0.5, i * 2 + 0.5, color="0.95", zorder=0.3)

    fig.supxlabel("V-score")
    ax.set_xscale("log")
    ax2.set_xscale("log")
    ax.set_xlim(*xlim1)
    ax2.set_xlim(*xlim2)
    ax.set_ylim(-1, y_max)
    ax2.set_ylim(-1, y_max)
    ax.set_xticks([1e-12, 1e-8, 1e-4])
    ax.set_xticks([v_score_exact_pos], minor=True)
    ax.set_xticklabels(["..."], minor=True)
    ax.xaxis.set_tick_params(which="minor", pad=2)
    ax.spines.right.set_visible(False)
    ax2.spines.left.set_visible(False)

    ax.set_yticks(range(y_max))
    ax.set_yticklabels(
        [show_ham_attr(x) for x in ham_attrs], fontfamily="monospace", fontsize="small"
    )
    ax.yaxis.set_tick_params(length=0)
    for i, text in enumerate(ax.get_yticklabels()):
        text.set_color(ham_colors[ham_attrs[i][0]])

    ax2.yaxis.set_tick_params(which="both", length=0)
    ax2.set_yticklabels([])

    d = 2
    kwargs = dict(
        clip_on=False,
        linestyle="",
        marker=[(-1, -d), (1, d)],
        markeredgecolor="k",
        markeredgewidth=0.8,
        markersize=6,
    )
    ax.plot([1, 1], [0, 1], transform=ax.transAxes, **kwargs)
    ax2.plot([0, 0], [0, 1], transform=ax2.transAxes, **kwargs)

    ax.grid(axis="x", color="0.8", linestyle="--")
    ax2.grid(axis="x", color="0.8", linestyle="--")
    ax.set_axisbelow(True)
    ax2.set_axisbelow(True)

    ax_symb = ax.twinx()
    ax_symb.spines.left.set_position(("outward", 11))
    ax_symb.spines.left.set_visible(False)
    ax_symb.spines.right.set_visible(False)
    ax_symb.spines.top.set_visible(False)
    ax_symb.spines.bottom.set_visible(False)
    ax_symb.yaxis.set_ticks_position("left")
    ax_symb.yaxis.set_tick_params(length=0)
    ax_symb.set_ylim(-1, y_max)
    ax_symb.set_yticks(range(y_max))
    ax_symb.set_yticklabels(
        [lat_types[x[1]] for x in ham_attrs],
        font="VarbenchIcons",
        fontsize="small",
    )
    for i, text in enumerate(ax_symb.get_yticklabels()):
        text.set_color(ham_colors[ham_attrs[i][0]])

    ax_left = ax.twinx()
    ax_left.spines.left.set_position(("outward", 42))
    ax_left.spines.left.set_visible(False)
    ax_left.spines.right.set_visible(False)
    ax_left.spines.top.set_visible(False)
    ax_left.spines.bottom.set_visible(False)
    ax_left.yaxis.set_ticks_position("left")
    ax_left.yaxis.set_tick_params(length=0)
    ax_left.set_ylim(-1, y_max)
    yticks = get_ax_left_yticks(ham_attrs)
    yticks[3] += 1
    yticks[4] -= 1
    yticks[5] -= 1
    ax_left.set_yticks(yticks)
    ax_left.set_yticklabels(
        ["TFIM", "Heisenberg", "$J_1$-$J_2$", "$t$-$V$", "Hubbard", "Impurity"],
        horizontalalignment="center",
        rotation=90,
        rotation_mode="anchor",
    )
    for i, text in enumerate(ax_left.get_yticklabels()):
        text.set_color(ham_colors[ham_types[i]])

    # fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")


if __name__ == "__main__":
    main()
