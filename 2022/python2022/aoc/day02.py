#!/usr/bin/env python
"""
Advent Of Code 2022 Day 02
https://adventofcode.com/2022/day/2
"""


def parse(filename):
    with open(filename) as file:
        return [parse_line(line.strip()) for line in file.readlines()]


def parse_line(line):
    return line.split(" ")


def score_pair(pair):
    p1 = pair[0]
    p2 = pair[1]
    lookup = {
        "X": "A",
        "Y": "B",
        "Z": "C",
    }
    p2 = lookup[p2]

    score1 = 0
    score2 = 0
    if p2 == "A":
        score1 = 1
    elif p2 == "B":
        score1 = 2
    elif p2 == "C":
        score1 = 3

    score2 = 3  # default to draw

    if p2 == "A":  # rock
        if p1 == "B":  # paper
            score2 = 0
        elif p1 == "C":  # scissors
            score2 = 6
    elif p2 == "B":  # paper
        if p1 == "A":  # rock
            score2 = 6
        elif p1 == "C":  # scissors
            score2 = 0
    elif p2 == "C":  # scissors
        if p1 == "A":  # rock
            score2 = 0
        elif p1 == "B":  # paper
            score2 = 6

    return score1 + score2


def score_pair2(pair):
    p1 = pair[0]
    want_to_do = pair[1]
    p2 = None

    if want_to_do == "X":
        # lose
        if p1 == "A":  # rock
            p2 = "C"  # scissors
        elif p1 == "B":  # paper
            p2 = "A"  # rock
        elif p1 == "C":  # scissors
            p2 = "B"  # paper
    elif want_to_do == "Y":
        # draw
        p2 = p1
    elif want_to_do == "Z":
        # win
        if p1 == "A":
            p2 = "B"
        elif p1 == "B":
            p2 = "C"
        elif p1 == "C":
            p2 = "A"

    score1 = 0
    score2 = 0
    if p2 == "A":
        score1 = 1
    elif p2 == "B":
        score1 = 2
    elif p2 == "C":
        score1 = 3

    score2 = 3  # default to draw

    if p2 == "A":  # rock
        if p1 == "B":  # paper
            score2 = 0
        elif p1 == "C":  # scissors
            score2 = 6
    elif p2 == "B":  # paper
        if p1 == "A":  # rock
            score2 = 6
        elif p1 == "C":  # scissors
            score2 = 0
    elif p2 == "C":  # scissors
        if p1 == "A":  # rock
            score2 = 0
        elif p1 == "B":  # paper
            score2 = 6

    # print(f"{score1} + {score2} = {score1 + score2}")
    return score1 + score2


class Day02:
    """AoC 2022 Day 02"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        score = 0
        for pair in data:
            score += score_pair(pair)
        return score

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        score = 0
        for pair in data:
            score += score_pair2(pair)
        return score
