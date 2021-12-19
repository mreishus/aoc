#!/usr/bin/env python
"""
Advent Of Code 2021 Day 19
https://adventofcode.com/2021/day/8
"""
from typing import List
import re
from collections import defaultdict
import numpy as np
from dataclasses import dataclass


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
    swap: int = 0  # 0 1 or 2 | I might only need 0 or 1
    roll: int = 0


def all_orientations():
    for swap in range(2):
        for roll in range(3):
            for fx in [False, True]:
                for fy in [False, True]:
                    for fz in [False, True]:
                        yield Orientation(fx=fx, fy=fy, fz=fz, swap=swap, roll=roll)


class Scanner:
    def __init__(self, scanner_num, coords):
        self.scanner_num = np.array(scanner_num)
        self.len = len(coords)
        self.coords = np.array(coords)
        self.coords_swap = self.build_coords_swap()
        # self.coords_swap2 = self.build_coords_swap2()
        self.node_i = 0

    def build_coords_swap(self):
        tmp = np.copy(self.coords)
        tmp[:, [1, 0]] = tmp[:, [0, 1]]
        return tmp

    def build_coords_swap2(self):
        tmp = np.copy(self.coords)
        tmp[:, [2, 0]] = tmp[:, [0, 2]]
        return tmp

    def add_entries(self, new_entries):
        # print("-coords-")
        # print(self.coords)
        # print("--new entries--")
        # print(new_entries)
        # print("--after--")
        # self.coords = np.concatenate((self.coords, new_entries))
        to_add = new_entries + self.coords[self.node_i]
        self.coords = np.concatenate((self.coords, to_add))
        self.coords = np.unique(self.coords, axis=0)
        # print(self.coords)
        self.coords_swap = self.build_coords_swap()

    def primary_view(self):
        # return self.coords
        return self.coords - self.coords[self.node_i]

    def all_views(self):
        for o in all_orientations():
            coords = self.get_coords(o)
            for node_i in range(self.len):
                yield (o, node_i, coords - coords[node_i])

    def get_coords(self, o: Orientation):
        id_ = np.array([1, 1, 1])
        tx = np.array([-1, 1, 1]) if o.fx else id_
        ty = np.array([1, -1, 1]) if o.fy else id_
        tz = np.array([1, 1, -1]) if o.fz else id_
        coords = self.coords
        if o.swap == 1:
            coords = self.coords_swap
        elif o.swap == 2:
            coords = self.coords_swap2
        return np.roll(coords * tx * ty * tz, o.roll, (1, 1))


def find_overlap(A, B):

    if not A.dtype == B.dtype:
        raise TypeError("A and B must have the same dtype")
    if not A.shape[1:] == B.shape[1:]:
        raise ValueError(
            "the shapes of A and B must be identical apart from " "the row dimension"
        )

    # reshape A and B to 2D arrays. force a copy if neccessary in order to
    # ensure that they are C-contiguous.
    A = np.ascontiguousarray(A.reshape(A.shape[0], -1))
    B = np.ascontiguousarray(B.reshape(B.shape[0], -1))

    # void type that views each row in A and B as a single item
    t = np.dtype((np.void, A.dtype.itemsize * A.shape[1]))

    # use in1d to find rows in A that are also in B
    return np.count_nonzero(np.in1d(A.view(t), B.view(t)))


def match(scan1, scan2):
    source = scan1.primary_view()
    match_max = 0
    node_i = None
    for o, i, target in scan2.all_views():
        match_count = find_overlap(source, target)
        if match_count > match_max:
            match_max = match_count
            node_i = i
            if match_count >= 12:
                pass
                # print("---source--")
                # print(source)
                # print("--target--")
                # print(target)
                # print(target)
                scan1.add_entries(target)
                # print("--primary view after merging--")
                # print(scan1.primary_view())
    return match_max


class Day19:
    """ AoC 2021 Day 19 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 19 part 1 """
        scan = parse(filename)
        # overlap_count = match(scan[0], scan[1])

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

        # # print(list(z.all_views()))
        # exit()

        # print("")
        # scan[0].fx = True
        # print(scan[0].get_coords())
        # print("")
        # scan[0].fx = True
        # z = scan[0].get_coords(Orientation())
        # y = z
        # print(z)
        # z[:, [2, 0]] = z[:, [0, 2]]
        # z[:, [1, 0]] = z[:, [0, 1]]
        # print(y)
        # print(z)
        # scan[1].coords += np.array([68, -1246, -430])
        # scan[1].coords_swap = scan[1].build_coords_swap()
        # print("ooo")
        # i = 0
        # for j in range(1, 5):
        #     print(f"Match[ {i} , {j} ] = {match(scan[i], scan[j])}")
        print("")
        for _ in range(6):
            for i in range(5):
                for j in range(5):
                    if i == j:
                        continue
                    z = match(scan[i], scan[j])
                    if z > 1:
                        print(f"Match[ {i} , {j} ] = {z}")
                    # print(np.shape(scan[i].coords), end=" ")
                    # print(np.shape(scan[j].coords))
                    # print("")
        # for i in range(5):
        #     for j in range(5):
        #         if i == j:
        #             continue
        #         print(f"Match[ {i} , {j} ] = {match(scan[i], scan[j])}")
        # for i in range(5):
        #     for j in range(5):
        #         if i == j:
        #             continue
        #         print(f"Match[ {i} , {j} ] = {match(scan[i], scan[j])}")
        print(scan[0].coords)
        return -1

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 19 part 2 """
        data = parse(filename)
        if len(data) < 20:
            print(data)
        return -1
