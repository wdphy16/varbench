#!/usr/bin/env python3

import os
from string import capwords

from collect import ham_types
from plot_v_score import get_dof
from reader import read_file, write_file

root = "../"


def my_capwords(s):
    if s == "DOF":
        return s
    return capwords(s)


def fix_headers(headers):
    fields = ["Energy", "Sigma", "Energy Variance", "Method", "Data Repository"]
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

            i = headers.index("Energy Variance") + 1
            dof = get_dof((ham_type, ham_param))
            headers = (*headers[:i], "DOF", *headers[i:])
            data = [(*x[:i], dof, *x[i:]) for x in data]

            write_file(file_path, headers, data, comments)


if __name__ == "__main__":
    main()
