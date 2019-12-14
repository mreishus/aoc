#!/usr/bin/env python
from collections import namedtuple, defaultdict

Element = namedtuple("Element", "thing quantity")
Rule = namedtuple("Rule", "materials result")


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    left, right = line.split(" => ")
    left = parse_elements(left)
    right = parse_elements(right)[0]
    return Rule(left, right)


def parse_elements(string):
    elements = string.split(", ")
    output = []
    for element in elements:
        quantity, thing = element.split(" ")
        output.append(Element(thing, int(quantity)))
    return output


def approx_match(d, elm):
    # We need ELM "28 A"
    # But there is no direct key in d corresponding to "28 A"
    # Find another one like "10 A"
    keys = [k for k, v in d.items() if k.thing == elm.thing]
    if len(keys) == 0:
        return None

    smaller = [k for k in keys if k.quantity <= elm.quantity]
    larger = [k for k in keys if k.quantity > elm.quantity]
    if len(smaller) > 0:
        return max(smaller, key=lambda x: x.quantity)
    if len(larger) > 0:
        return max(larger, key=lambda x: x.quantity)
    print(
        f"Can't find a match keys[{keys}] smaller[{smaller}] larger[{larger}] elmQ[{elm.quantity}]"
    )
    raise ValueError("Approx_match: The world is wrong")


def part2(rules):
    # Manual Binary Search
    try_me = [1_993_284]
    for v in try_me:
        a = part1(rules, v)
        print(f"fuel {v} answer {a} answer {a / 1_000_000_000}")


def part1(rules, initial_fuel=1):
    d = {rule.result: rule.materials for rule in rules}
    inventory = defaultdict(int, {"FUEL": initial_fuel})
    negatives = defaultdict(int)

    while True:
        for (elem_thing, elem_quantity) in list(inventory.items()):
            if elem_quantity < 0:
                raise ValueError("Shouldn't happen")
            if elem_quantity == 0:
                del inventory[elem_thing]
                continue

            elm = Element(elem_thing, elem_quantity)
            if elem_thing in negatives:
                # Use leftovers
                new_amount = elem_quantity + negatives[elem_thing]
                if new_amount >= 0:
                    inventory[elem_thing] = new_amount
                    del negatives[elem_thing]
                else:
                    del inventory[elem_thing]
                    negatives[elem_thing] = new_amount
            elif elm in d:
                # Direct replacement
                for (new_thing, new_amount) in d[elm]:
                    inventory[new_thing] += new_amount
                del inventory[elem_thing]
            elif approx_match(d, elm):
                # We have an approx match; use_this = 10 A, produces = 10 ORE, but
                # we have say, 14 A (or 8 A!)
                use_this = approx_match(d, elm)
                produces = d[use_this]

                # print(f"  --USE THIS --> [{use_this}] ")
                # print(f"   <--- GET THIS [{produces}]")

                # Add the new stuff we made
                times = max(elm.quantity // use_this.quantity, 1)
                for produced_elm in produces:
                    inventory[produced_elm.thing] += produced_elm.quantity * times

                # Take away what we used
                new_amount = elm.quantity - use_this.quantity * times
                if new_amount >= 0:
                    inventory[elem_thing] = new_amount
                else:
                    # print(f"     -- Hmm.. producing waste.")
                    del inventory[elem_thing]
                    negatives[elem_thing] += new_amount
                break

        if len([k for k, v in inventory.items() if v > 0]) == 1:
            break
    return inventory["ORE"]


if __name__ == "__main__":
    # rules = parse("../input_p1_165.txt")
    rules = parse("../input.txt")
    print("Part1: ")
    print(part1(rules))

    print("Part2: ")
    print(part2(rules))
