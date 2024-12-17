#!/usr/bin/env python
"""
Advent Of Code 2024 Day 17
https://adventofcode.com/2024/day/17
"""
from typing import List
import re
from collections import defaultdict

class OP:
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

class Computer:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.outputs = []
        self.pc = 0
        self.state = "new"

    def get_combo(self, i):
        if i == 0:
            return 0
        elif i == 1:
            return 1
        elif i == 2:
            return 2
        elif i == 3:
            return 3
        elif i == 4:
            return self.a
        elif i == 5:
            return self.b
        elif i == 6:
            return self.c
        else:
            raise ValueError

    def execute(self):
        if self.state == "halted":
            print("Refusing to execute; is halted")
        self.state = "running"
        while True:
            # print("Iter", self.pc)
            if self.pc >= len(self.program):
                print(" .. halted")
                self.state = "halted"
                break
            # print("Did not halt")
            instruction = self.program[self.pc]
            operand = self.program[self.pc + 1]
            # operand = None
            # if self.pc+1 < len(self.program):

            if instruction == OP.ADV:
                num = self.a
                denom = 2 ** self.get_combo(operand)
                self.a = num // denom
                self.pc += 2
            elif instruction == OP.BXL:
                operand = self.program[self.pc + 1]
                self.b ^= operand
                self.pc += 2
            elif instruction == OP.BST:
                self.b = self.get_combo(operand) % 8
                self.pc += 2
            elif instruction == OP.JNZ:
                if self.a == 0:
                    pass
                    self.pc += 2
                else:
                    self.pc = operand
                    ## Do not PC inc
            elif instruction == OP.BXC:
                self.b ^= self.c
                self.pc += 2
            elif instruction == OP.OUT:
                self.outputs.append( self.get_combo(operand) % 8 )
                self.pc += 2
            elif instruction == OP.BDV:
                num = self.a
                denom = 2 ** self.get_combo(operand)
                self.b = num // denom
                self.pc += 2
            elif instruction == OP.CDV:
                num = self.a
                denom = 2 ** self.get_combo(operand)
                self.c = num // denom
                self.pc += 2

def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))

def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    data = []
    lines = string.split("\n")
    return ints(lines[0])[0], ints(lines[1])[0], ints(lines[2])[0], ints(lines[4])

class Day17:
    """AoC 2024 Day 17"""

    @staticmethod
    def part1(filename: str) -> int:
        (a, b, c, program) = parse(filename)

        # print("")
        # c1 = Computer(123, 2024, 43690, [4, 0])
        # print(c1.a, c1.b, c1.c)
        # c1.execute()
        # print(c1.a, c1.b, c1.c)
        # print(c1.outputs)
        # exit()

        # print(a, b, c)
        # print(program)
        # exit()
        cpu = Computer(a, b, c, program)
        cpu.execute()

        string = ""
        for o in cpu.outputs:
            string = string + str(o) + ","
        return string

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        print(data)
        return -1
