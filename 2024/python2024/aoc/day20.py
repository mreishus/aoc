#!/usr/bin/env python
"""
Advent Of Code 2024 Day 20
https://adventofcode.com/2024/day/20
"""
from collections import deque, defaultdict

class Grid:
    def __init__(self):
        self.grid = {}
        self.max_x = 0
        self.max_y = 0
        self.start = (-1, -1)
        self.end = (-1, -1)
        self.dist_map = {}

    def parse(self, filename: str):
        x = 0
        y = 0

        with open(filename) as file:
            for line in file:
                for char in line.strip():
                    if char == 'S':
                        self.start = (x, y)
                        self.grid[(x, y)] = '.'
                    elif char == 'E':
                        self.end = (x, y)
                        self.grid[(x, y)] = '.'
                    else:
                        self.grid[(x, y)] = char
                    x += 1
                    self.max_x = max(self.max_x, x)
                y += 1
                x = 0
                self.max_y = max(self.max_y, y)

    def bfs_simple(self, start_loc):
        queue = deque([
            (start_loc, 0)
        ])
        visited = set()
        edge_to = {start_loc: None}
        while queue:
            loc, steps = queue.pop()
            (x, y) = loc

            if loc in visited:
                continue
            visited.add(loc)

            if (x, y) == self.end:
                path = []
                current = loc
                while current is not None:
                    path.append(current)
                    current = edge_to[current]
                return path[::-1], steps

            for xx, yy in self.get_neighbors(x, y):
                next_loc = (xx, yy)
                if next_loc not in edge_to:
                    edge_to[next_loc] = loc
                    queue.append( ((xx, yy), steps + 1) )
        return None, None

    def bfs2(self, start_loc):
        c1loc = (None, None)
        c2loc = (None, None)
        queue = deque([
            (start_loc, 0, c1loc, c2loc)
        ])

        visited = set()
        cheats_found_end = set()
        cheat_times = {}

        while queue:
            loc, steps, c1loc, c2loc = queue.popleft()
            (x, y) = loc

            if (loc, c1loc, c2loc) in visited:
                continue
            visited.add((loc, c1loc, c2loc))

            if (c1loc, c2loc) in cheats_found_end:
                continue

            if (x, y) == self.end:
                cheats_found_end.add((c1loc, c2loc ))
                cheat_times[ (c1loc, c2loc) ] = steps
                continue

            # Already cheated
            if ( c1loc != (None, None) and c2loc != (None, None) ):
                dist_to_end = self.dist_map[x, y]
                queue.append( ( self.end, steps + dist_to_end, c1loc, c2loc ) )

            # Regular step
            if (
                ( c1loc == (None, None) and c2loc == (None, None) )
            ):
                for xx, yy in self.get_neighbors(x, y):
                    queue.append( ((xx, yy), steps + 1, c1loc, c2loc) )

            # Start Cheat
            if c1loc == (None, None):
                for xx, yy in self.start_cheat(x, y):
                    queue.append( ((xx, yy), steps + 1, (xx, yy), c2loc) )

            # End Cheat
            if c2loc == (None, None) and c1loc != (None, None):
                for xx, yy in self.end_cheat(x, y):
                    queue.append( ((xx, yy), steps + 1, c1loc, (xx, yy)) )

        return cheat_times

    def get_neighbors_raw(self, x, y):
        for (dx, dy) in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
            if (x + dx, y + dy) in self.grid:
                yield (x+dx, y+dy)

    def get_neighbors(self, x, y):
        for (xx, yy) in self.get_neighbors_raw(x, y):
            if self.grid[ (xx, yy) ] != '#':
                yield (xx, yy)

    def start_cheat(self, x, y):
        for (xx, yy) in self.get_neighbors_raw(x, y):
            if self.grid[ (xx, yy) ] == '#':
                yield (xx, yy)

    def end_cheat(self, x, y):
        for (xx, yy) in self.get_neighbors_raw(x, y):
            if self.grid[ (xx, yy) ] != '#':
                yield (xx, yy)

    def populate_distance_map(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in self.dist_map:
                    continue
                if self.grid[(x, y)] == '#':
                    continue
                path, steps = self.bfs_simple((x, y))
                for (xx, yy) in path:
                    self.dist_map[(xx, yy)] = steps
                    steps -= 1

class Day20:
    """AoC 2024 Day 20"""

    @staticmethod
    def part1(filename: str) -> int:
        g = Grid()
        g.parse(filename)
        g.populate_distance_map()

        cheat_times = g.bfs2(g.start)

        no_cheat_time = cheat_times[ ( (None, None), (None, None) ) ]
        save = defaultdict(int)
        for x in cheat_times.keys():
            time = cheat_times[x]
            time_saved = no_cheat_time - time
            save[time_saved] += 1

        save_100 = 0
        for k in sorted(save.keys()):
            print (k, save[k])
            if k >= 100:
                save_100 += save[k]
        return save_100

    @staticmethod
    def part2(filename: str) -> int:
        return -1
