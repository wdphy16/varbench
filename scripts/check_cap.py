#!/usr/bin/env python3

from collect import data_key, get_data


def main():
    data = get_data()
    data.sort(key=data_key)

    ham_attrs = set()
    ham_attrs_lower = set()
    for row in data:
        ham_attr = row[:2]
        if ham_attr in ham_attrs:
            continue

        ham_attrs.add(ham_attr)

        if "X" in row[1]:
            print(ham_attr)

        ham_attr_lower = (row[0], row[1].lower())
        if ham_attr_lower in ham_attrs_lower:
            print(ham_attr)
        else:
            ham_attrs_lower.add(ham_attr_lower)


if __name__ == "__main__":
    main()
