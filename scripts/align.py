#!/usr/bin/env python3

import os

from collect import ham_types
from reader import read_file, write_file

root = "../"


def main():
    for _dir in os.scandir(root):
        if _dir.name not in ham_types:
            continue

        for file in os.scandir(_dir):
            if not file.is_file() or file.name == "README.md":
                continue

            file_path = os.path.join(root, _dir.name, file.name)
            print(file_path)

            headers, data, comments = read_file(file_path)
            while comments and not comments[0]:
                del comments[0]

            write_file(file_path, headers, data, comments)


if __name__ == "__main__":
    main()
