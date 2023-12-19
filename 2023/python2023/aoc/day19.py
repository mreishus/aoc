#!/usr/bin/env python
"""
Advent Of Code 2023 Day 19
https://adventofcode.com/2023/day/19
"""
import re
from typing import List
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
        workflow_name, conditions = workflow.split("{")
        conditions = conditions[:-1]
        conditions = conditions.split(",")
        for condition in conditions:
            condition = condition.split(":")
            parsed_workflows[workflow_name].append(condition)
    return parsed_workflows


def parse_ratings(ratings):
    """
    {x=787,m=2655,a=1222,s=2876}
    {x=1679,m=44,a=2067,s=496}
    {x=2036,m=264,a=79,s=2244}
    """
    ## Make one list per line.
    ratings = ratings.split("\n")
    ## Remove the brackets.
    ratings = [rating[1:-1] for rating in ratings]
    ## Split on commas.
    ratings = [rating.split(",") for rating in ratings]
    ## Split on equals.
    ratings = [[rating.split("=") for rating in rating] for rating in ratings]
    ## Convert to dict.
    ratings = [{rating[0]: rating[1] for rating in rating} for rating in ratings]
    return ratings


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


class Day19:
    """AoC 2023 Day 19"""

    @staticmethod
    def part1(filename: str) -> int:
        workflows, ratings = parse(filename)

        accepted = []
        rejected = []
        next_flow = "in"
        for line in ratings:
            print("1111111 Line:", line)
            while next_flow != "A" and next_flow != "R":
                rules = workflows[next_flow]
                for rule in rules:
                    # print(" 222 Flow: ", next_flow)
                    # print(" Rule:", rule)
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
                    print(" 333 Flow: ", next_flow)
            print("444 Flow: ", next_flow)
            if next_flow == "A":
                accepted.append(line)
            else:
                rejected.append(line)
            next_flow = "in"

        total = 0
        for line in accepted:
            total += sum(map(int, line.values()))
        return total

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return -1
