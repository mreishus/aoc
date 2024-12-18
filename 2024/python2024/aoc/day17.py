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
            if self.pc >= len(self.program):
                # print(" .. halted")
                self.state = "halted"
                break
            # print("Did not halt")
            instruction = self.program[self.pc]
            operand = self.program[self.pc + 1]
            # print(f"pc={self.pc} i={instruction} b={self.b}")
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

        (a, b, c, program) = parse(filename)
        """
        Program: 2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0
        Program: 2,4 ,1,5 ,7,5 ,1,6 ,4,1 ,5,5 ,0,3 ,3,0

        [0]  2 4 b = a % 8
        [2]  1 5 b = b ^ 5
        [4]  7 5 c = a // (2 ** b)
        [6]  1 6 b = b ^ 6
        [8]  4 1 b = b ^ c
        [10] 5 5 output: b % 8
        0 3 a = a // (2 ** 3)
        3 0 jump to beginning unless A is 0
        """

        def get_outputs(this_a):
            cpu = Computer(this_a, b, c, program)
            cpu.execute()
            return cpu.outputs

        iii = 0
        for z in range(8):
            for y in range(8):
                for x in range(8):
                    for v in range(8):
                        for u in range(8):
                            for t in range(8):
                                for m in range(8):
                                    a  = 3 * 8**15
                                    a += 0 * 8**14
                                    a += 3 * 8**13
                                    a += 3 * 8**12
                                    a += 0 * 8**11
                                    a += 4 * 8**10
                                    a += 6 * 8**9
                                    a += 3 * 8**8
                                    a += 3 * 8**7
                                    a += m * 8**6
                                    a += t * 8**5
                                    a += u * 8**4
                                    a += v * 8**3
                                    a += x * 8**2
                                    a += y * 8**1
                                    a += z * 8**0
                                    g = get_outputs(a)
                                    iii += 1
                                    if iii % 300000 == 0:
                                        print(g, program)
                                    if g == program:
                                        print("FOUND")
                                        print(a)

        # I Used this to help get the top ones
        # # print('  got:' + str(get_outputs(a)))
        # print("")
        # print(' want:' + str(program))
        # for x in range(10):
        #     a = 0
        #     a += 3 * 8**15
        #     a += 0 * 8**14
        #     a += 3 * 8**13
        #     a += 3 * 8**12
        #     a += 0 * 8**11
        #     a += 4 * 8**10
        #     a += 6 * 8**9
        #     a += 3 * 8**8
        #     a += 3 * 8**7
        #     a += 0 * 8**6
        #     a += 0 * 8**5
        #     a += 0 * 8**4
        #     a += 0 * 8**3
        #     a += 0 * 8**2
        #     a += 0 * 8**1
        #     a += 0 * 8**0
        #
        #     g = get_outputs(a)
        #     print('  got:' + str(get_outputs(a)) + ' ' + str(x) + ' ' + str(a))
