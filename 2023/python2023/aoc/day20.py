#!/usr/bin/env python
"""
Advent Of Code 2023 Day 20
https://adventofcode.com/2023/day/20
"""
import re
from typing import List
from collections import defaultdict, namedtuple

PulseBase = namedtuple("Pulse", ["to", "level", "frm"])


class Pulse(PulseBase):
    def __repr__(self):
        level_str = "high" if self.level == 1 else "low"
        return f"{self.frm} -{level_str}-> {self.to}"


class Module:
    def __init__(self, name, mtype, outputs):
        self.name = name
        self.mtype = mtype
        self.outputs = outputs

        if mtype == "flipflop":
            self.state = False
            self.input_states = None
        elif mtype == "conjunction":
            self.state = None
            self.input_states = {}
        else:
            self.state = None
            self.input_states = None

    def __repr__(self):
        if self.mtype == "flipflop":
            return f"Module<{self.name} {self.mtype} -> {self.outputs} ({self.state})>"
        elif self.mtype == "conjunction":
            return f"Module<{self.name} {self.mtype} -> {self.outputs} ({self.input_states})>"
        else:
            return f"Module<{self.name} {self.mtype} -> {self.outputs} ({self.state})>"


class Collection:
    def __init__(self, modules):
        self.modules = modules
        self.pulses = []
        self.pulse_count = 0
        self.pulse_low_count = 0
        self.pulse_high_count = 0
        self.button_count = 0

    def __repr__(self):
        return f"Collection<{self.modules}>"

    def init_conjunctions(self):
        for mod in self.modules.values():
            if mod.mtype == "conjunction":
                ## Find all modules with this as an output
                connected = []
                for other in self.modules.values():
                    if mod.name in other.outputs:
                        connected.append(other)
                mod.input_states = {m.name: 0 for m in connected}

    def display(self):
        for mod in self.modules.values():
            print(mod)

    def push_button(self):
        ## Find the broadcaster
        broadcaster = None
        for mod in self.modules.values():
            if mod.mtype == "broadcast":
                broadcaster = mod
                break
        if broadcaster is None:
            raise Exception("No broadcaster found")

        self.button_count += 1
        pulse = Pulse(broadcaster.name, 0, None)
        self.pulses.append(pulse)
        self.process_pulses()

    def process_pulses(self, debug=False):
        while len(self.pulses) > 0:
            pulse = self.pulses.pop(0)
            if debug:
                print(f"Pulse: {pulse}")
            self.process_pulse(pulse)
            self.pulse_count += 1
            if pulse.level == 0:
                self.pulse_low_count += 1
            else:
                self.pulse_high_count += 1

    def magic_number(self):
        return self.pulse_low_count * self.pulse_high_count

    def process_pulse(self, pulse):
        if pulse.to == "rx" and pulse.level == 0:
            print(f"Button pressed {self.button_count} times")
            return self.button_count

        if pulse.to not in self.modules:
            # print(f"Warning: Module {pulse.to} not found")
            return
        mod = self.modules[pulse.to]
        if mod.mtype == "broadcast":
            self.process_broadcast(mod, pulse)
        elif mod.mtype == "conjunction":
            self.process_conjunction(mod, pulse)
        elif mod.mtype == "flipflop":
            self.process_flipflop(mod, pulse)
        else:
            raise Exception("Unknown module type")

    def process_broadcast(self, mod, pulse):
        level = pulse.level
        for output in mod.outputs:
            new_pulse = Pulse(output, level, mod.name)
            self.pulses.append(new_pulse)

    def process_flipflop(self, mod, pulse):
        level = pulse.level
        ## If level is high, ignore.
        if level == 1:
            return
        ## If level is low, its state flips.
        mod.state = not mod.state
        ## If new state is on, send a high pulse to all outputs.
        ## If new state if off, send a low pulse to all outputs.
        for output in mod.outputs:
            new_pulse = Pulse(output, 1 if mod.state else 0, mod.name)
            self.pulses.append(new_pulse)

    def process_conjunction(self, mod, pulse):
        interesting = ["th", "sv", "gh", "ch"]

        level = pulse.level
        ## When a pulse is received, update its memory for that input.
        mod.input_states[pulse.frm] = level

        ## If all inputs are high, send a low pulse to all outputs.
        ## If any input is low, send a high pulse to all outputs.
        if all(mod.input_states.values()):
            for output in mod.outputs:
                new_pulse = Pulse(output, 0, mod.name)
                self.pulses.append(new_pulse)
        else:
            for output in mod.outputs:
                if mod.name in interesting:
                    print(
                        f"{mod.name} Sending high pulse to {output} | {self.button_count}"
                    )
                new_pulse = Pulse(output, 1, mod.name)
                self.pulses.append(new_pulse)


def parse(filename: str):
    with open(filename) as file:
        mods = {}
        for line in file.readlines():
            mod = parse_line(line.strip())
            mods[mod.name] = mod
        return mods


def parse_line(line):
    left, right = line.split(" -> ")

    mod = None
    if left[0] == "&":
        mod = Module(left[1:], "conjunction", right.split(", "))
    elif left[0] == "%":
        mod = Module(left[1:], "flipflop", right.split(", "))
    else:
        mod = Module(left, "broadcast", right.split(", "))

    return mod


class Day20:
    """AoC 2023 Day 20"""

    @staticmethod
    def part1(filename: str) -> int:
        data = parse(filename)
        c = Collection(data)
        c.init_conjunctions()

        for i in range(1000):
            c.push_button()
        print(c.magic_number())

        return -1

    @staticmethod
    def part2(filename: str) -> int:
        data = parse(filename)
        c = Collection(data)
        c.init_conjunctions()

        for i in range(999999999):
            if i % 10000 == 0:
                print(f"Pushing button {i} times")
            c.push_button()
        return -1


"""
&th -> cn
&sv -> cn
&gh -> cn
&ch -> cn

Pushing button 0 times
ch Sending high pulse to cn | 3917
gh Sending high pulse to cn | 3943
th Sending high pulse to cn | 3947
sv Sending high pulse to cn | 4001
ch Sending high pulse to cn | 7834
gh Sending high pulse to cn | 7886
th Sending high pulse to cn | 7894
sv Sending high pulse to cn | 8002
Pushing button 10000 times
ch Sending high pulse to cn | 11751
gh Sending high pulse to cn | 11829
th Sending high pulse to cn | 11841
sv Sending high pulse to cn | 12003
ch Sending high pulse to cn | 15668
gh Sending high pulse to cn | 15772
th Sending high pulse to cn | 15788
sv Sending high pulse to cn | 16004
ch Sending high pulse to cn | 19585
gh Sending high pulse to cn | 19715
th Sending high pulse to cn | 19735
Pushing button 20000 times
sv Sending high pulse to cn | 20005
ch Sending high pulse to cn | 23502
gh Sending high pulse to cn | 23658
th Sending high pulse to cn | 23682
sv Sending high pulse to cn | 24006

sv Sending high pulse to cn | 4001
sv Sending high pulse to cn | 8002
sv Sending high pulse to cn | 12003
sv Sending high pulse to cn | 16004
sv Sending high pulse to cn | 20005
sv Sending high pulse to cn | 24006

ch Sending high pulse to cn | 3917
ch Sending high pulse to cn | 7834
ch Sending high pulse to cn | 11751
ch Sending high pulse to cn | 15668
ch Sending high pulse to cn | 19585
ch Sending high pulse to cn | 23502

gh Sending high pulse to cn | 3943
gh Sending high pulse to cn | 7886
gh Sending high pulse to cn | 11829
gh Sending high pulse to cn | 15772
gh Sending high pulse to cn | 19715
gh Sending high pulse to cn | 23658

th Sending high pulse to cn | 3947
th Sending high pulse to cn | 7894
th Sending high pulse to cn | 11841
th Sending high pulse to cn | 15788
th Sending high pulse to cn | 19735
th Sending high pulse to cn | 23682


sv = +4001 each time.
ch = +3917 each time.
gh = +3943
th = +3947

np.lcm.reduce([4001, 3917, 3943, 3947]) = 243902373381257
"""
