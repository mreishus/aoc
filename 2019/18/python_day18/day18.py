#!/usr/bin/env python

import string
from collections import namedtuple, defaultdict
import networkx as nx
from heapdict import heapdict

# A path between two keys contains a length (int) and a list of doors along
# that path (List of strings)
PathInfo = namedtuple("PathInfo", ("length", "doors"))

# A state in our final search contains our hero locations and the collected
# keys (frozenset)
State = namedtuple("State", ("location", "collected_keys"))

# A Edge, a possible action to take in our final search, brings us to a new
# state with cost `length` of steps
Edge = namedtuple("Edge", ("state", "length"))


class Maze:
    def __init__(self, filename):
        self.grid = None
        self.graph = None
        self.loc_of_door = None
        self.door_of_loc = None
        self.loc_of_key = None
        self.hero_locs = []
        self.parse(filename)

    def parse(self, filename):
        """ Given a filename, read the grid and fill out many variables.

        grid: dictionary with complex numbers representing coords as keys,
        characters as values.
        loc_of_door: Hash with door names as keys, complex coordinates as values.
        loc_of_key: Hash with key names as keys, complex coordinates as values.
        door_of_loc: Hash with complex coordinates as keys, door names as values.
        all_keys: Frozenset of all keys seen.
        hero_locs: List of all hero locations (complex coordinates).
        """
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
        """ For build_graph().  Is a character valid to walk on?
        See through all doors: the only "invalid" chars are walls. """
        return char != "#"

    def gen_coords(self, grid):
        """ Given a dictionary with keys as complex numbers representing
        coorindates, return a generator iterating over all coordinates in x, y
        format.  Assumes the grid is not sparse. """
        reals = [c.real for c in grid.keys()]
        imags = [c.imag for c in grid.keys()]
        for y in range(int(min(imags)), int(max(imags)) + 1):
            for x in range(int(min(reals)), int(max(reals)) + 1):
                yield x, y

    def gen_neighbors(self, coord):
        """ Given a complex coordinate, return a generator iterating over
        its 4 direct neighbors """
        yield coord + complex(0, -1)
        yield coord + complex(0, 1)
        yield coord + complex(-1, 0)
        yield coord + complex(1, 0)

    def build_graph(self):
        """ Iterate over the grid and build a networkx graph of
        adjoining spaces, pretending that doors do not exist.
        We will use this to find the path between all sets of keys. """
        G = nx.Graph()

        for x, y in self.gen_coords(self.grid):
            location = complex(x, y)
            if location not in self.grid:
                continue
            char = self.grid[location]
            if not self.valid_char(char):
                continue

            G.add_node(location)

            for neighbor in self.gen_neighbors(location):
                neighbor_char = self.grid[neighbor]
                if self.valid_char(neighbor_char):
                    G.add_edge(location, neighbor)

        self.graph = G

    def find_doors_on_path(self, path):
        """ Given a path (a list of complex coordinates), return a frozenset
        containing all doors on that path.
        Example input value:  [ [(43+3j), (43+2j), (43+1j), (44+1j), (45+1j),
        (46+1j), ... ]
        Example return value: frozenset({'v', 'h', 'u', 'p'})
        """
        return frozenset(
            [
                self.door_of_loc[step].lower()
                for step in path
                if step in self.door_of_loc
            ]
        )

    def build_key_paths(self):
        """ Examine all pairs of keys and calculate the shortest path between
        them, if one exists.  Save the length of that path, and any doors along
        that path, in self.path_info. """
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
        """ Main solver.  Run Dijkstra's algorithm between all nodes containing
        State, or a list of hero locations and a frozenset of all keys
        collected. We assume the paths between all keys has already been
        calculated in self.path.info. """
        dist_to = defaultdict(lambda: 999_999_999)
        edge_to = {}
        queue = heapdict()

        collected_keys = frozenset({})
        state = State(tuple(self.hero_locs), collected_keys)
        dist_to[state] = 0
        queue[state] = 0
        while len(queue) > 0:
            (state, length) = queue.popitem()

            # Stop searching if solution
            if state.location == complex(-1, -1):
                break

            # loc_string = "".join(state.collected_keys)
            # print(f"{dist_to[state]:>7} {str(state.location):12} {loc_string}")

            steps = self.possible_edges(state)
            for new_state, length in steps:
                if dist_to[new_state] > dist_to[state] + length:
                    dist_to[new_state] = dist_to[state] + length
                    edge_to[new_state] = state
                    queue[new_state] = dist_to[new_state]

        print("==Done==")
        for k, v in dist_to.items():
            # -1, -1 represents the solved state: All keys collected.
            if k.location == complex(-1, -1):
                print(f"{v} {k}")
                return v
        return 0

    def possible_edges(self, state):
        """ Given a State (list of hero locations and keys collected), what the
        steps we can take from that state? A Edge() contains a new state and
        the number of steps taken to get to that state. """
        (locations, collected_keys) = state
        steps = []
        remaining_keys = self.all_keys - collected_keys

        # Special case: Free move to -1, -1 if collected all keys to indicate
        # problem is solved
        if len(remaining_keys) == 0 and locations != complex(-1, -1):
            new_state = State(complex(-1, -1), collected_keys)
            steps.append(Edge(new_state, 0))

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
            steps.append(Edge(new_state, info.length))
        return steps


if __name__ == "__main__":
    # f = Maze("../input_small.txt")
    # f = Maze("../input_86.txt")
    # f = Maze("../input_136.txt")
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
