#!/usr/bin/env python
"""
Advent Of Code 2023 Day 19
https://adventofcode.com/2023/day/19
"""
from collections import defaultdict


def parse(filename: str):
    with open(filename) as file:
        lines = file.read().strip()
        workflows, ratings = lines.split("\n\n")
        return parse_workflows(workflows), parse_ratings(ratings)


def parse_workflows(workflows):
    """
    px{a<2006:qkq,m>2090:A,rfg}
    pv{a>1716:R,A}
    lnx{m>1548:A,A}
    rfg{s<537:gd,x>2440:R,A}
    qs{s>3448:A,lnx}
    """
    workflows = workflows.split("\n")
    parsed_workflows = defaultdict(list)
    for workflow in workflows:
        workflow_name, conds = workflow.split("{")
        conds = conds[:-1]
        conds = conds.split(",")
        for cond in conds:
            cond = cond.split(":")
            parsed_workflows[workflow_name].append(cond)
    return parsed_workflows


def parse_ratings(ratings):
    """
    {x=787,m=2655,a=1222,s=2876}
    {x=1679,m=44,a=2067,s=496}
    {x=2036,m=264,a=79,s=2244}
    """
    ## Remove the brackets, split on commas
    ratings = [rating[1:-1].split(",") for rating in ratings.split("\n")]
    ## Split on equals.
    ratings = [[rating.split("=") for rating in rating] for rating in ratings]
    ## Convert to dict.
    ratings = [{rating[0]: rating[1] for rating in rating} for rating in ratings]
    return ratings


def process(line, workflows):
    next_flow = "in"
    while next_flow != "A" and next_flow != "R":
        rules = workflows[next_flow]
        for rule in rules:
            ## Base case.
            if len(rule) == 1:
                next_flow = rule[0]
                break

            ## Look for < in rule.
            if "<" in rule[0]:
                field, value = rule[0].split("<")
                if int(line[field]) < int(value):
                    next_flow = rule[1]
                    break

            ## Look for > in rule.
            if ">" in rule[0]:
                field, value = rule[0].split(">")
                if int(line[field]) > int(value):
                    next_flow = rule[1]
                    break
    return next_flow


def xmas_lookup(char):
    table = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3,
    }
    return table[char]


def process_split(
    workflows,
    begin_flow="in",
    consider_low=None,
    consider_high=None,
):
    if consider_low is None:
        consider_low = [1, 1, 1, 1]
    if consider_high is None:
        consider_high = [4000, 4000, 4000, 4000]

    next_flow = begin_flow
    extras = []

    while next_flow != "A" and next_flow != "R":
        rules = workflows[next_flow]
        for rule in rules:
            ## Base case.
            if len(rule) == 1:
                next_flow = rule[0]
                break

            ## Look for < in rule.
            if "<" in rule[0]:
                field, value = rule[0].split("<")
                i = xmas_lookup(field)

                ### Three cases: Value is within range, value is too low, value is too high.

                if consider_high[i] < int(value):
                    ## Always pass.
                    next_flow = rule[1]
                    break
                elif consider_low[i] >= int(value):
                    ## Always fail.
                    pass
                else:
                    ## Split.
                    pass_low = consider_low.copy()
                    pass_high = consider_high.copy()
                    pass_low[i], pass_high[i] = consider_low[i], int(value) - 1

                    these = process_split(workflows, rule[1], pass_low, pass_high)
                    extras.extend(these)

                    consider_low[i], consider_high[i] = int(value), consider_high[i]

            if ">" in rule[0]:
                field, value = rule[0].split(">")
                i = xmas_lookup(field)

                ### Three cases: Value is within range, value is too low, value is too high.

                if consider_low[i] > int(value):
                    ## Always pass.
                    next_flow = rule[1]
                    break
                elif consider_high[i] <= int(value):
                    ## Always fail.
                    pass
                else:
                    ## Split.
                    pass_low = consider_low.copy()
                    pass_high = consider_high.copy()
                    pass_low[i], pass_high[i] = int(value) + 1, consider_high[i]

                    these = process_split(workflows, rule[1], pass_low, pass_high)
                    extras.extend(these)

                    consider_low[i], consider_high[i] = consider_low[i], int(value)

    ranges = []
    if next_flow == "A":
        ranges.append((consider_low, consider_high))
    return ranges + extras


class Day19:
    """AoC 2023 Day 19"""

    @staticmethod
    def part1(filename: str) -> int:
        workflows, ratings = parse(filename)

        accepted = []
        rejected = []
        for line in ratings:
            result = process(line, workflows)
            if result == "A":
                accepted.append(line)
            else:
                rejected.append(line)

        total = 0
        for line in accepted:
            total += sum(map(int, line.values()))
        return total

    @staticmethod
    def part2(filename: str) -> int:
        workflows, _ratings = parse(filename)
        result = process_split(workflows, "in")

        combos = 0
        for rge in result:
            xs = abs(rge[0][0] - rge[1][0]) + 1
            ms = abs(rge[0][1] - rge[1][1]) + 1
            as_ = abs(rge[0][2] - rge[1][2]) + 1
            ss = abs(rge[0][3] - rge[1][3]) + 1

            these_combos = xs * ms * as_ * ss
            combos += these_combos
        return combos
