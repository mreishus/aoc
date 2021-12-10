#!/usr/bin/env python
"""
Advent Of Code 2021 Day 10
https://adventofcode.com/2021/day/10
"""


def parse(filename: str):
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


def corrupted_score(line):
    score = {
        "]": 57,
        "}": 1197,
        ">": 25137,
        ")": 3,
    }
    pairs = {
        "[": "]",
        "{": "}",
        "<": ">",
        "(": ")",
    }
    openers = pairs.keys()
    closers = pairs.values()
    q = []
    for char in line:
        if char in openers:
            q.append(char)
        elif char in closers:
            match_me = q.pop()
            if pairs[match_me] != char:
                return score[char]
    return 0


def complete(line):
    scores = {
        "]": 2,
        "}": 3,
        ">": 4,
        ")": 1,
    }
    pairs = {
        "[": "]",
        "{": "}",
        "<": ">",
        "(": ")",
    }
    openers = pairs.keys()
    closers = pairs.values()
    q = []
    for char in line:
        if char in openers:
            q.append(char)
        elif char in closers:
            match_me = q.pop()
            if pairs[match_me] != char:
                raise ValueError
    score = 0
    while len(q) > 0:
        match_me = q.pop()
        to_add = pairs[match_me]
        score *= 5
        score += scores[to_add]
    return score


class Day10:
    """ AoC 2021 Day 10 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 10 part 1 """
        data = parse(filename)
        score = 0
        for line in data:
            score += corrupted_score(line)
        return score

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 10 part 2 """
        data = parse(filename)
        valid_data = []
        scores = []
        for line in data:
            if corrupted_score(line) > 0:
                continue
            score = complete(line)
            scores.append(score)
        scores = sorted(scores)
        return scores[len(scores) // 2]
