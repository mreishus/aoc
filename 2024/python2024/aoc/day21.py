#!/usr/bin/env python
"""
Advent Of Code 2024 Day 21
https://adventofcode.com/2024/day/21
"""
from aoc.heapdict import heapdict
from collections import defaultdict, namedtuple

State = namedtuple("State", ("numloc", "code", "arrowlocs"))

class KeypadNum:
    def __init__(self):
        self.numgrid = {
            (0, 0): 7,
            (1, 0): 8,
            (2, 0): 9,
            (0, 1): 4,
            (1, 1): 5,
            (2, 1): 6,
            (0, 2): 1,
            (1, 2): 2,
            (2, 2): 3,
            # (0, 3): ?, # Not there
            (1, 3): 0,
            (2, 3): 'A',
        }
        self.begin_loc = (2, 3)

        self.arrowgrid = {
            #(0, 0): 7, # Not There
            (1, 0): '^',
            (2, 0): 'A',
            (0, 1): '<',
            (1, 1): 'v',
            (2, 1): '>',
        }
        self.begin_loc_arrow = (2, 0)
        self.n = 2
        self.begin_loc_arrows = tuple((2, 0) for _ in range(self.n))

    def search(self, final_code):
        self.target_code = tuple(list(final_code))
        final_code = tuple(list(final_code))

        init_state = State(self.begin_loc, (), self.begin_loc_arrows)

        dist_to = defaultdict(lambda: 999_999)
        edge_to = defaultdict(list)  # a list of previous states for each state
        open_set = heapdict()
        dist_to[init_state] = 0
        open_set[init_state] = 0
        final_state = None  # Store the final state when we find it

        while len(open_set) > 0:
            (state, length) = open_set.popitem()
            (numloc, code, arrow_locs) = state
            # print(state)
            if code == final_code:
                final_state = state
                break  # We found our target
            for (new_state, cost, name) in self.next_states(state):
                if dist_to[new_state] > dist_to[state] + cost:
                    dist_to[new_state] = dist_to[state] + cost
                    edge_to[new_state] = (state, name)
                    open_set[new_state] = dist_to[new_state]

        if final_state is None:
            return 0, []

        # Reconstruct the path
        path = []
        current_state = final_state
        while current_state in edge_to:
            prev_state, move = edge_to[current_state]
            path.append(move)
            current_state = prev_state

        path.reverse()  # Since we built it backwards
        return len(path), path

    def next_states(self, state):
        numloc = state.numloc
        output = state.code
        arrowlocs = state.arrowlocs

        returns = []
        valid = len(output) <= len(self.target_code) and all(a == b for a, b in zip(output, self.target_code))
        if not valid:
            return []

        dirs = {
            '^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0),
        }

        i = self.n - 1

        # Outermost: can move it
        (x, y) = arrowlocs[i]
        for (dir_name, (dx, dy)) in dirs.items():
            if (dx+x, dy+y) in self.arrowgrid:
                new_arrows = tuple( list(arrowlocs[:-1]) + [(dx+x, dy+y)] )
                new_state = State(numloc, output, new_arrows)
                returns.append(( new_state, 1, dir_name))

        # Outermost: Can press
        while i >= 0:
            (x, y) = arrowlocs[i]
            under_arrow = self.arrowgrid[(x, y)]
            # print(f"i={i} under_arrow={under_arrow}")
            if under_arrow in dirs:
                (dx, dy) = dirs[under_arrow]
                # Cause i-1 to move
                j = i - 1
                # print(f"  considering j={j}")

                # Normal case: j >= 0, so dealing with another arrowpad
                if j >= 0:
                    (xx, yy) = arrowlocs[j]
                    if (dx+xx, dy+yy) in self.arrowgrid:
                        # print(f"  decided to move arrowloc {j}")
                        new_arrows = tuple(
                            list(arrowlocs[:j]) + [(dx+xx, dy+yy)] + list(arrowlocs[j+1:])
                        )
                        new_state = State(numloc, output, new_arrows)
                        returns.append((new_state, 1, 'A'))
                    else:
                        pass
                        # print(f"  cannot move arrowloc {j} because {dx+xx},{dy+yy} is not in arrowgrid")
                    break
                elif j == -1:
                    # Special Case: j = -1, so move the numpad
                    (xx, yy) = numloc
                    if (dx+xx, dy+yy) in self.numgrid:
                        new_state = State((dx+xx, dy+yy), output, arrowlocs)
                        returns.append((new_state, 1, 'A'))
                    break
                else:
                    raise ValueError()
            elif under_arrow == "A":
                # Cause the next robot to press
                # print(f"  since under_arrow is A, decrementing without doing anything else")
                i -= 1
            else:
                raise ValueError()

        if i == -1:
            # Only allow pressing 'A' if the resulting code would still be a valid prefix
            digit = str(self.numgrid[numloc])
            new_output = tuple(list(output) + [digit])
            if len(new_output) <= len(self.target_code) and all(a == b for a, b in zip(new_output, self.target_code)):
                new_state = State(numloc, new_output, arrowlocs)
                returns.append(( new_state, 1, 'A'))

        # print('--')
        # print('Input state: ', state)
        # for r in returns:
        #     print(r)
        return returns


class KeypadArrow:
    def __init__(self):
        self.grid = {}

    def fill(self):
        self.grid = {
            #(0, 0): 7, # Not There
            (1, 0): '^',
            (2, 0): 'A',
            (0, 1): '<',
            (1, 1): 'v',
            (2, 1): '>',
        }
        self.begin_loc = (2, 0)


def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    return string.split("\n")

class Day21:
    """AoC 2024 Day 21"""

    @staticmethod
    def part1(filename: str) -> int:

        # test_state2 = State(numloc=(2, 3), code=(), arrowlocs=((1, 0), (2, 0)))
        # kn = KeypadNum()
        # kn.target_code ='3'
        # kn.next_states(test_state2)
        # return

        codes = parse(filename)
        total = 0
        for code in codes:
            kn = KeypadNum()
            (ln, path) = kn.search( code )
            numeric = int(code[:3])
            total += numeric * ln
        return total

    @staticmethod
    def part2(filename: str) -> int:
        pass
