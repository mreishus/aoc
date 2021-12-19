#!/usr/bin/env python
"""
Advent Of Code 2021 Day 19
https://adventofcode.com/2021/day/8
"""
from typing import List
import re
from dataclasses import dataclass
import numpy as np


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


def parse(filename: str):
    with open(filename) as file:
        return [parse_block(block) for block in file.read().strip().split("\n\n")]


def parse_block(block):
    lines = block.split("\n")
    scanner_num = ints(lines.pop(0))[0]
    coords = [ints(line) for line in lines]
    return Scanner(scanner_num, coords)


@dataclass
class Orientation:
    fx: bool = False
    fy: bool = False
    fz: bool = False
    swap: int = 0  # 0 or 1
    roll: int = 0


def all_orientations():
    """ Returns 48 orientations instead of 24 """
    for swap in range(2):
        for roll in range(3):
            for fx in [False, True]:
                for fy in [False, True]:
                    for fz in [False, True]:
                        yield Orientation(fx=fx, fy=fy, fz=fz, swap=swap, roll=roll)


class Scanner:
    def __init__(self, scanner_num, coords):
        self.scanner_num = scanner_num
        self.len = len(coords)
        self.coords = np.array(coords, dtype=np.int32)
        self.coords_swap = self.build_coords_swap()

        self.solved = False
        self.offset = np.array([0, 0, 0], dtype=np.int32)
        self.orient = Orientation()

    def solve(self, offset, orient):
        self.solved = True
        self.offset = offset
        self.orient = orient

    def build_coords_swap(self):
        tmp = np.copy(self.coords)
        tmp[:, [1, 0]] = tmp[:, [0, 1]]
        return tmp

    def real_view_relative(self, source_i):
        c = self.real_view()
        return c - c[source_i]

    def real_view(self):
        if not self.solved:
            raise ValueError
        return self.get_coords(self.orient) + self.offset

    def all_views(self):
        for o in all_orientations():
            coords = self.get_coords(o)
            for node_i in range(self.len):
                yield (o, node_i, coords - coords[node_i])

    def get_coords(self, o: Orientation):
        id_ = np.array([1, 1, 1], dtype=np.int32)
        tx = np.array([-1, 1, 1], dtype=np.int32) if o.fx else id_
        ty = np.array([1, -1, 1], dtype=np.int32) if o.fy else id_
        tz = np.array([1, 1, -1], dtype=np.int32) if o.fz else id_
        coords = self.coords
        if o.swap == 1:
            coords = self.coords_swap
        return np.roll(coords * tx * ty * tz, o.roll, (1, 1))


def find_overlap(A, B):
    s = set()
    for row in A:
        s.add(row.tobytes())
    count = 0
    for row in B:
        if row.tobytes() in s:
            count += 1
    return count


def match(scan1, scan2):
    match_max = 0
    found = False
    for source_i in range(len(scan1.coords)):
        source = scan1.real_view_relative(source_i)
        for orient, target_i, target in scan2.all_views():
            match_count = find_overlap(source, target)
            if match_count > match_max:
                match_max = match_count
                if match_count >= 12:
                    return source_i, target_i, orient, match_count
        if found:
            break
    return None, None, Orientation(), match_max


class Day19:
    """ AoC 2021 Day 19 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 19 part 1 """
        scan = parse(filename)
        scan[0].solved = True
        size = len(scan)

        ## Orientation Checker:
        # z = Scanner(0, [[1, 2, 3]])
        # col = []
        # s = set()
        # for a, b in z.all_views():
        #     bb = b[0].tolist()
        #     strv = ", ".join(map(str, bb))
        #     s.add(strv)
        #     col.append(strv)
        # print(len(col))
        # print(len(s))
        # exit()

        print()
        solved = set([0])
        no_match = set()
        while len(solved) < size:
            for i in solved.copy():
                for j in range(size):
                    if j in solved or (i, j) in no_match:
                        continue
                    print(f"Checking {i} {j}")
                    source_i, target_i, orient, match_count = match(scan[i], scan[j])
                    if match_count >= 12:
                        print(f"SOLVING {i} ---> {j}")
                        print(f"Match[ {i} , {j} ] = {match_count}")
                        print(f"source_i={source_i} target_i={target_i} orient{orient}")
                        offset1 = scan[i].real_view()[source_i]
                        offset2 = scan[j].get_coords(orient)[target_i]
                        j_location = offset1 - offset2
                        print(j_location)
                        scan[j].solve(j_location, orient)
                        solved.add(j)
                    else:
                        no_match.add((i, j))

        first = solved.pop()
        all_coords = scan[first].real_view()
        for i in solved:
            all_coords = np.concatenate((all_coords, scan[i].real_view()))
        all_coords_uniq = np.unique(all_coords, axis=0)
        print(f"Part1 Answer={len(all_coords_uniq)}")

        max_dist = 0
        for i in range(size):
            for j in range(i, size):
                if i == j:
                    next
                diff = scan[i].offset - scan[j].offset
                dist = np.sum(np.abs(diff))
                max_dist = max(max_dist, dist)
        print(f"Part2 Answer={max_dist}")
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 19 part 2 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return -1
