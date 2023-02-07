#!/usr/bin/env python3

import os

from add_dof import my_capwords
from collect import ham_types
from plot_v_score import get_energy_inf
from reader import read_file, write_file

root = "../"


def fix_headers(headers):
    fields = ["Energy", "Sigma", "Energy Variance", "DOF", "Method", "Data Repository"]
    fields_lower = [x.lower() for x in fields]
    out = []
    for col in headers:
        try:
            out.append(my_capwords(fields[fields_lower.index(col.lower())]))
        except ValueError:
            out.append(col)
    return out


def main():
    for _dir in os.scandir(root):
        if _dir.name not in ham_types:
            continue
        ham_type = _dir.name

        for file in os.scandir(_dir):
            if not file.is_file() or file.name == "README.md":
                continue
            ham_param = file.name.replace(".md", "")

            file_path = os.path.join(root, _dir.name, file.name)
            print(file_path)

            headers, data, comments = read_file(file_path)
            headers = fix_headers(headers)
            while comments and not comments[0]:
                del comments[0]

            i = headers.index("DOF") + 1
            energy_inf = get_energy_inf((ham_type, ham_param))
            headers = (*headers[:i], "Einf", *headers[i:])
            data = [(*x[:i], f"{energy_inf:.15g}", *x[i:]) for x in data]

            write_file(file_path, headers, data, comments)


if __name__ == "__main__":
    main()
