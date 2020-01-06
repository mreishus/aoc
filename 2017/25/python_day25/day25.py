#!/usr/bin/env python
from typing import Tuple, Dict, Any
from collections import defaultdict
import re
import pprint


def parse(filename: str):
    rules_for_state = {}
    with open(filename) as file:
        paragraphs = file.read().split("\n\n")
        (initial_state, steps) = parse_first_paragraph(paragraphs[0])
        for para in paragraphs[1:]:
            (state, rules) = parse_paragraph(para)
            rules_for_state[state] = rules
    return (initial_state, steps, rules_for_state)


def parse_first_paragraph(text: str):
    return ("A", 12586542)


def parse_paragraph(text: str):
    """
    Returns a tuple of (state, rules), something like:
    ( 'A', {
        0: {'write': 1, 'move': 1, 'new_state': 'B'},
        1: {'write': 0, 'move': -1, 'new_state': 'B'}
    } )
    """
    state_m = re.match(r"In state (\w+):(.*)", text, re.DOTALL)
    if state_m is None:
        return None
    (state, text) = state_m.groups()

    text_blocks = re.findall(
        r"If the current value is \d:.*?(?=If the current value|$)", text, re.DOTALL
    )
    rules = {}
    for text_block in text_blocks:
        (condition, actions) = parse_block(text_block)
        rules[condition] = actions
    return (state, rules)


def parse_block(text) -> Tuple[int, Dict[str, Any]]:
    """
    Takes a "text block", which looks like:

    If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state B.

    Returns something like:
    (0, {'write': 1, 'move': 1, 'new_state': 'B'})
    or
    (1, {'write': 0, 'move': -1, 'new_state': 'B'})
    """
    condition_m = re.match("If the current value is (\d+):", text)
    if condition_m is None:
        return None
    condition = int(condition_m.groups()[0])

    write_m = re.search("Write the value (\d+)", text)
    move_m = re.search("Move one slot to the (left|right)", text)
    new_state_m = re.search("Continue with state (\w+)", text)
    if write_m is None or move_m is None or new_state_m is None:
        return None

    actions = {
        "write": int(write_m.groups()[0]),
        "move": translate_move(move_m.groups()[0]),
        "new_state": new_state_m.groups()[0],
    }
    return (condition, actions)


def translate_move(move):
    if move == "left":
        return -1
    if move == "right":
        return 1
    raise ValueError("Don't understand move")


class TuringMachine:
    def __init__(
        self, state: str, steps: int, rules: Dict[str, Dict[int, Dict[str, Any]]]
    ):
        self.state = state
        self.steps = steps
        self.rules = rules
        self.tape = defaultdict(lambda: 0)
        self.loc = 0

    def step(self):
        value = self.tape[self.loc]
        actions = self.rules[self.state][value]
        # Actions Will have 'write' 'move' 'new_state' keys
        self.tape[self.loc] = actions["write"]
        self.loc += actions["move"]
        self.state = actions["new_state"]

    def all_steps(self):
        for i in range(self.steps):
            self.step()

    def checksum(self):
        return list(self.tape.values()).count(1)


if __name__ == "__main__":
    (initial_state, steps, rules) = parse("../input.txt")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rules)
    tm = TuringMachine(initial_state, steps, rules)
    tm.all_steps()
    print(tm.checksum())
