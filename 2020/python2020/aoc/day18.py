#!/usr/bin/env python
"""
Advent Of Code 2020 Day 18
https://adventofcode.com/2020/day/18
"""

import re


def parse(filename):
    with open(filename) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line):
    t = Tokenizer(line)
    return [tt for tt in t.get_tokens()]


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.original_text = text

    def get_tokens(self):
        match_missing = False

        while len(self.text) > 0 and not match_missing:
            if match := re.match(r"(\d+)\s*", self.text):
                self.text = self.text[match.end() :]
                token = int(match.groups()[0])
                yield token
            elif match := re.match(r"([*+(\)])\s*", self.text):
                self.text = self.text[match.end() :]
                token = match.groups()[0]
                yield token
            else:
                match_missing = True


def p1_operator_higher_pri(left_op, right_op):
    """ Returns true if left_op has higher priority in p1 rules """
    # Both operators have equal priority
    # But since left associative, the left one "wins"
    return True


def p2_operator_higher_pri(left_op, right_op):
    """ Returns true if left_op has higher priority in p2 rules """
    pri = {
        "+": 9000,
        "*": 1,
    }
    return pri[left_op] >= pri[right_op]


def p1_eval(tokens):
    return eval(tokens, p1_operator_higher_pri)


def p2_eval(tokens):
    return eval(tokens, p2_operator_higher_pri)


def eval(tokens, op_higher_pri):
    """ Shunting-yard algorithm: Infix -> RPN """
    output = []
    operators = []

    while len(tokens) > 0:
        a_tok = tokens.pop(0)
        if isinstance(a_tok, int):
            output.append(a_tok)
        elif a_tok in ("*", "+"):
            while (
                len(operators) > 0
                and operators[-1] != "("
                and op_higher_pri(operators[-1], a_tok)
            ):
                output.append(operators.pop())
            operators.append(a_tok)
        elif a_tok == "(":
            operators.append(a_tok)
        elif a_tok == ")":
            while operators[-1] != "(":
                output.append(operators.pop())
            if operators[-1] == "(":
                operators.pop()

    while len(operators) > 0:
        output.append(operators.pop())

    return rpn(output)


def rpn(queue):
    stack = []
    operands = {
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
    }

    for item in queue:
        if isinstance(item, int):
            stack.append(item)
        elif item in operands:
            a = stack.pop()
            b = stack.pop()
            answer = operands[item](a, b)
            stack.append(answer)
    return stack[-1]


class Day18:
    """ AoC 2020 Day 18 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2020 day 18 part 1 """
        data = parse(filename)
        total = 0
        for equation in data:
            total += p1_eval(equation)
        return total

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2020 day 18 part 2 """
        data = parse(filename)
        total = 0
        for equation in data:
            total += p2_eval(equation)
        return total
