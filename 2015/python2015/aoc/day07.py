#!/usr/bin/env python
"""
Advent Of Code 2015 Day 7
https://adventofcode.com/2015/day/7
"""

import operator
import copy
from typing import Any, Callable, Dict, Union
from dataclasses import dataclass
from aoc.parsers import all_lines

OPS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift,
    "NOT": operator.invert,
    "ID": lambda x: x,
}


def try_parse_int(s, base=10):
    try:
        return int(s, base)
    except ValueError:
        return s


@dataclass
class Gate:
    """
    Example: x RSHIFT 5 -> aa

    arg1: "x"
    arg2: 5
    output "aa"
    operator: operator.rshift
    arity: 2
    done: False
    """

    line: str
    arg1: Union[int, str]
    arg2: Union[int, str]
    output: str
    operator: Callable[[Any], Any]
    arity: int
    done: bool


def parse_line(line: str):
    [left, right] = line.split(" -> ")
    left = left.split(" ")
    if len(left) == 3:
        # Example: "u LSHIFT 1"
        [arg1, an_operator, arg2] = left
        arg1 = try_parse_int(arg1)
        arg2 = try_parse_int(arg2)
        return Gate(line, arg1, arg2, right, OPS[an_operator], 2, False)
    if len(left) == 2:
        # Example: "NOT dq"
        [an_operator, arg1] = left
        arg1 = try_parse_int(arg1)
        return Gate(line, arg1, None, right, OPS[an_operator], 1, False)
    if len(left) == 1:
        # Example: "1500"
        [arg1] = left
        arg1 = try_parse_int(arg1)
        return Gate(line, arg1, None, right, OPS["ID"], 1, False)
    return None


def lookup(wires: Dict[str, int], arg1: Union[str, int]) -> Union[int, None]:
    if isinstance(arg1, int):
        return arg1
    if arg1 in wires:
        return wires[arg1]
    return None


def solve(commands, b_override=None):
    wires = {}
    commands = copy.deepcopy(commands)
    done_count = 0
    while True:
        for gate in commands:
            if gate.done:
                continue
            if b_override is not None:
                wires["b"] = b_override
            if gate.arity == 2:
                arg1 = lookup(wires, gate.arg1)
                arg2 = lookup(wires, gate.arg2)
                if arg1 is not None and arg2 is not None:
                    wires[gate.output] = gate.operator(arg1, arg2) & 0xFFFF
                    gate.done = True
                    done_count += 1
            elif gate.arity == 1:
                arg1 = lookup(wires, gate.arg1)
                if arg1 is not None:
                    wires[gate.output] = gate.operator(arg1) & 0xFFFF
                    gate.done = True
                    done_count += 1
        if done_count == len(commands):
            break
    return wires


def part1(commands):
    wires = solve(commands)
    return wires["a"]


def part2(commands):
    wires1 = solve(commands)
    wires2 = solve(commands, wires1["a"])
    return wires2["a"]


class Day07:
    """ AoC 2015 Day 07 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 07 part 1 """
        commands = [parse_line(line) for line in all_lines(filename)]
        return part1(commands)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 07 part 2 """
        commands = [parse_line(line) for line in all_lines(filename)]
        return part2(commands)
