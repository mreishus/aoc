#!/usr/bin/env python
"""
Advent Of Code 2020 Day 16
https://adventofcode.com/2020/day/16
"""

import re
import numpy as np


def parse(filename):
    with open(filename) as f:
        lines = f.read().strip()
        rules, your_ticket, nearby_tickets = lines.split("\n\n")

        rules = parse_rules(rules)

        yt_preamble = "your ticket:\n"
        if your_ticket.startswith(yt_preamble):
            your_ticket = your_ticket[len(yt_preamble) :].strip()
            your_ticket = [int(x) for x in your_ticket.split(",")]
        else:
            raise "Cant parse your ticket"

        nbt_preamble = "nearby tickets:\n"
        if nearby_tickets.startswith(nbt_preamble):
            nearby_tickets = nearby_tickets[len(nbt_preamble) :].strip()
            t = []
            for line in nearby_tickets.split("\n"):
                t.append([int(x) for x in line.split(",")])
            nearby_tickets = t
        else:
            raise "Cant parse nearby tickets"

        return rules, your_ticket, nearby_tickets


def parse_rules(rules_in):
    # "row: 6 - 11 or 33 - 44"
    rules_out = []
    for line in rules_in.split("\n"):
        (name, r1, r2, r3, r4) = re.match(
            r"(.*?): (\d+)-(\d+) or (\d+)-(\d+)", line
        ).groups()
        rules_out.append(Rule(name, r1, r2, r3, r4))

    return rules_out


class Rule:
    def __init__(self, name, r1, r2, r3, r4):
        self.name = name
        self.r1 = int(r1)
        self.r2 = int(r2)
        self.r3 = int(r3)
        self.r4 = int(r4)

    def __repr__(self):
        return f"<Rule {self.name}, {self.r1}-{self.r2} OR {self.r3}-{self.r4}>"

    def __hash__(self):
        return hash(self.name)

    def is_valid(self, val):
        return (self.r1 <= val <= self.r2) or (self.r3 <= val <= self.r4)


def p1(data):
    rules, _your_ticket, nearby_tickets = data
    error_rate = 0

    for ticket in nearby_tickets:
        for num in ticket:
            if not any(r.is_valid(num) for r in rules):
                error_rate += num
    return error_rate


def p2(data):
    rules, your_ticket, nearby_tickets = data

    def is_valid_ticket(ticket):
        for num in ticket:
            if not any(r.is_valid(num) for r in rules):
                return False
        return True

    ## Filter Invalid Tickets
    nearby_tickets = list(filter(is_valid_ticket, nearby_tickets))

    ## Find Rules
    tickets_t = np.array(nearby_tickets).T.tolist()  # transpose
    rules_assigned = {}  # rule -> column number of data
    while len(rules_assigned) < len(rules):
        for col_i, values in enumerate(tickets_t):
            # print(f"Examining {col_i} {values}")
            matches = []
            for rule in rules:
                if rule in rules_assigned:
                    continue
                if all(rule.is_valid(num) for num in values):
                    # print(f"Possible Match: {rule.name}")
                    matches.append(rule)
            if len(matches) == 1:
                rule = matches[0]
                # print(f"Definite Match: {rule.name}")
                rules_assigned[rule] = col_i

    answer = 1
    # print(rules_assigned)
    for rule, col_i in rules_assigned.items():
        if rule.name.startswith("departure"):
            answer *= your_ticket[col_i]
    return answer


class Day16:
    """ AoC 2020 Day 16 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 16 part 1 """
        data = parse(filename)
        return p1(data)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 16 part 2 """
        data = parse(filename)
        return p2(data)
