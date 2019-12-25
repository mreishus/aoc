#!/usr/bin/env python
from itertools import combinations

items = [
    "hypercube",
    "coin",
    "klein bottle",
    "shell",
    "easter egg",
    "astrolabe",
    "tambourine",
    "dark matter",
]

for n in range(9):
    print("")
    for these_items in list(combinations(items, n)):
        print("")
        for item in these_items:
            print(f"take {item}")
        print("south")
        for item in these_items:
            print(f"drop {item}")
