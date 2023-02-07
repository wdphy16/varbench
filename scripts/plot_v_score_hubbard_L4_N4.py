#!/usr/bin/env python3

import re

from matplotlib import pyplot as plt

from collect import data_key, get_data
from plot_v_score import get_v_score

out_filename = "./v_score_hubbard_L4_N4.pdf"

Us = [2, 4, 6, 8, 10]
known_methods = {
    "DMRG": "DMRG",
}
colors = {
    "DMRG": "C0",
}


def main():
    data = get_data()
    data.sort(key=data_key)

    v_scores = {}
    for row in data:
        ham_type, ham_param, method = row[:3]
        for k, v in known_methods.items():
            if method.startswith(k):
                method = v
                break
        else:
            continue

        if ham_type != "Hubbard":
            continue

        match = re.compile(r"square_16_P_4_([-.\d]+)").fullmatch(ham_param)
        if not match:
            continue
        U = float(match.group(1))

        v_score = get_v_score(row)
        v_scores[(U, method)] = v_score

    fig, ax = plt.subplots(figsize=(6, 4))

    for method, color in colors.items():
        ys = [v_scores[(U, method)] for U in Us]
        ax.plot(Us, ys, label=method, color=color, marker="x")

    ax.set_title("Hubbard, 4x4, PP, N_up = N_down = 4")
    ax.set_xlabel("U")
    ax.set_ylabel("V-score")
    ax.set_yscale("log")
    ax.grid()
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_filename, bbox_inches="tight")


if __name__ == "__main__":
    main()
