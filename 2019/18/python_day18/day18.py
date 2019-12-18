#!/usr/bin/env python
import string
import networkx as nx
from heapq import heappush, heappop
from collections import namedtuple, defaultdict
from heapdict import heapdict

PathInfo = namedtuple('PathInfo', ('length', 'doors'))
State = namedtuple('State', ('location', 'collected_keys'))
Step = namedtuple('Step', ('state', 'length'))

class Maze:
    def __init__(self, filename):
        self.grid = None  # defaultdict(lambda: "?")
        self.graph = None
        self.loc_of_door = None
        self.door_of_loc = None
        self.loc_of_key = None
        self.between_keys = None
        self.hero_locs = []
        self.parse(filename)

    def parse(self, filename):
        grid = {}
        loc_of_door = {}
        loc_of_key = {}
        location = complex(0, 0)

        with open(filename) as f:
            for line in f:
                for char in line.strip():
                    # print(char)
                    grid[location] = char

                    if char in string.ascii_uppercase:
                        loc_of_door[char] = location
                    if char in string.ascii_lowercase:
                        loc_of_key[char] = location
                    if char == "@":
                        self.hero_locs.append(location)
                    location += complex(1, 0)
                location += complex(0, 1)
                location = complex(0, location.imag)

        self.grid = grid
        self.loc_of_door = loc_of_door
        self.loc_of_key = loc_of_key
        self.door_of_loc = dict(map(reversed, self.loc_of_door.items()))
        self.all_keys = frozenset(loc_of_key.keys())

    def valid_char(self, char):
        if char == "?" or char == "#":
            return False
        # See through all doors:
        # Check for doors later
        # if char in string.ascii_uppercase: # and char not in self.unlocked_doors:
        #     return False
        return True

    def build_graph(self):
        G = nx.Graph()

        reals = [c.real for c in self.grid.keys() if self.grid[c] != "?"]
        imags = [c.imag for c in self.grid.keys() if self.grid[c] != "?"]
        for y in range(int(min(imags)) - 1, int(max(imags)) + 1):
            for x in range(int(min(reals)) - 1, int(max(reals)) + 1):
                location = complex(x, y)
                if location not in self.grid:
                    continue
                char = self.grid[location]
                if not self.valid_char(char):
                    continue

                G.add_node(location)

                up = location + complex(0, -1)
                down = location + complex(0, 1)
                left = location + complex(-1, 0)
                right = location + complex(1, 0)

                for neighbor in [up, down, left, right]:
                    neighbor_char = self.grid[neighbor]
                    if self.valid_char(neighbor_char):
                        G.add_edge(location, neighbor)

        self.graph = G
        return G

    def find_doors_on_path(self, path):
        return frozenset([self.door_of_loc[step].lower() for step in path if step in self.door_of_loc])

    def build_key_paths(self):
        G = self.graph
        important_locs = list(self.loc_of_key.values()) + self.hero_locs
        path_info = {}

        for loc1 in important_locs:
            for loc2 in important_locs:
                if loc1 == loc2 or (loc1, loc2) in path_info:
                    continue
                path = None
                try:
                    path = nx.dijkstra_path(G, loc1, loc2)
                except nx.NetworkXNoPath:
                    continue
                steps_taken = len(path) - 1
                doors_on_path = self.find_doors_on_path(path)

                path_info[(loc1, loc2)] = PathInfo(steps_taken, doors_on_path)
                path_info[(loc2, loc1)] = PathInfo(steps_taken, doors_on_path)
        self.path_info = path_info

    def solve(self):
        dist_to = defaultdict(lambda: 999_999_999)
        edge_to = {}
        hd = heapdict()

        collected_keys = frozenset({})
        state = State(tuple(self.hero_locs), collected_keys)
        dist_to[state] = 0
        hd[state] = 0
        while len(hd) > 0:
            (state, length) = hd.popitem()
            steps = self.possible_steps(state)
            for new_state, length in steps:
                if dist_to[new_state] > dist_to[state] + length:
                    dist_to[new_state] = dist_to[state] + length
                    edge_to[new_state] = state
                    hd[new_state] = dist_to[new_state]

        print("==Done==")
        # for k, v in edge_to.items():
        #     print(f"{v} {k}")
        for k, v in dist_to.items():
            if k.location == complex(-1, -1):
                print(f"{v} {k}")
                return v
        return 0


    def possible_steps(self, state):
        (locations, collected_keys) = state
        steps = []
        remaining_keys = self.all_keys - collected_keys

        # Special case: Free move to -1, -1 if collected all keys to indicate
        # problem is solved
        if len(remaining_keys) == 0 and locations != complex(-1, -1):
            new_state = State(complex(-1, -1), collected_keys)
            steps.append(Step(new_state, 0))

        for key in remaining_keys:

            info = None
            loc_to_update = None
            for i, this_location in enumerate(locations):
                pair = (this_location, self.loc_of_key[key])
                if pair in self.path_info:
                    info = self.path_info[pair]
                    loc_to_update = i

            blocking_doors = info.doors - collected_keys
            if len(blocking_doors) > 0:
                continue

            new_locations = list(locations)
            new_locations[loc_to_update] = self.loc_of_key[key]
            new_locations = tuple(new_locations)

            new_state = State(new_locations, collected_keys | frozenset({key}))
            steps.append(Step(new_state, info.length))
        return steps

if __name__ == "__main__":
    #f = Maze("../input_small.txt")
    #f = Maze("../input_86.txt")
    #f = Maze("../input_136.txt")

    f = Maze("../input.txt")
    print("Part1:")
    f.build_graph()
    f.build_key_paths()
    print(f.solve())

    f = Maze("../input_p2.txt")
    print("Part2:")
    f.build_graph()
    f.build_key_paths()
    print(f.solve())
    # print(f.path_info)
    # print(f.all_keys)
    # print(f.grid)
    # print(f.build_graph().edges())
