#!/usr/bin/env python3

from glob import glob

paths = glob("./**/*.md", recursive=True)
for path in sorted(paths):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    dirty = False

    is_stripe = False

    for idx in range(len(lines)):
        line = lines[idx]

        todo = "TODO: This is from Sorella and this is not public "
        if todo not in line:
            continue

        # script_path = path
        # script_path = script_path.replace(
        #     "./",
        #     "https://github.com/varbench/methods/blob/main/scripts/",
        # )
        # script_path = script_path.replace(".md", "/vmc_2DgatedtensorizedRNN.sh")
        # if "VMC with stripe" in line:
        #     script_path = script_path.replace(".md", "/VMC-stripes/vmc_hubbard.sh")
        #     is_stripe = True
        # elif "VMC" in line:
        #     script_path = script_path.replace(".md", "/VMC-uniform/vmc_hubbard.sh")
        #     is_stripe = False
        # else:
        #     if is_stripe:
        #         script_path = script_path.replace(".md", "/FN-stripes/fn_hubbard.sh")
        #     else:
        #         script_path = script_path.replace(".md", "/FN-uniform/fn_hubbard.sh")

        # line = line.replace(todo, f"[code]({script_path})")
        line = line.replace(
            todo,
            "[paper](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.107.115133) [code](",
        )
        line = line.replace("pbc |", "pbc) |")

        lines[idx] = line
        dirty = True

    if not dirty:
        continue

    lines.append("")
    text = "\n".join(lines)
    print(path)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
