#!/usr/bin/env python3

import os
import re
from glob import glob

paths = glob("./**/*.md", recursive=True)
for path in sorted(paths):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        for match in re.compile(r"\[code\]\(([^\)]+)\)").finditer(text):
            link = match.group(1)
            if not link.startswith("https://github.com/varbench/methods/blob/main/"):
                continue
            link = link.replace(
                "https://github.com/varbench/methods/blob/main/", "../varbench_methods/"
            )

            if not os.path.exists(link):
                print(link)

        if text.count("(") != text.count(")"):
            print("Unbalance", path)
