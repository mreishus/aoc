#!/usr/bin/env python
"""
Advent Of Code 2015 Day 14
https://adventofcode.com/2015/day/14
"""

import re
import itertools
import copy
from dataclasses import dataclass
from typing import Iterator
from aoc.parsers import all_lines

# Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
PARSER = re.compile(
    r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds"
)


class Deer:
    def __init__(self, name: str, speed: int, active_time: int, rest_time: int):
        self.name = name
        self.speed = speed
        self.active_time = active_time
        self.rest_time = rest_time
        self.position = 0
        self.points = 0
        self._seq = self._sequence()

    def __repr__(self):
        return str(self.__dict__)

    def _sequence(self) -> Iterator[int]:
        move = itertools.repeat(self.speed, self.active_time)
        rest = itertools.repeat(0, self.rest_time)
        return itertools.cycle(itertools.chain(move, rest))

    def move(self):
        self.position += next(self._seq)


def parse_line(line: str) -> Deer:
    match = re.search(PARSER, line)
    if not match:
        raise ValueError("Can't parse line")
    (name, speed, active_time, rest_time) = match.group(1, 2, 3, 4)
    return Deer(name, int(speed), int(active_time), int(rest_time))


def race_winner_distance(deers, steps):
    deers = copy.deepcopy(deers)
    for _ in range(steps):
        for deer in deers:
            deer.move()
    winner = max(deers, key=lambda deer: deer.position)
    return winner.position


def race_winner_points(deers, steps):
    deers = copy.deepcopy(deers)
    for _ in range(steps):
        for deer in deers:
            deer.move()
        # There might be ties; find the first winner then look for all deers matching that position
        a_winner = max(deers, key=lambda deer: deer.position)
        winners = [deer for deer in deers if deer.position == a_winner.position]
        for this_winner in winners:
            this_winner.points += 1

    winner = max(deers, key=lambda deer: deer.points)
    return winner.points


class Day14:
    """ AoC 2015 Day 14 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 14 part 1 """
        deers = [parse_line(line) for line in all_lines(filename)]
        return race_winner_distance(deers, 2503)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 14 part 2 """
        deers = [parse_line(line) for line in all_lines(filename)]
        return race_winner_points(deers, 2503)
