#!/usr/bin/env python
"""
Advent Of Code 2024 Day 21
https://adventofcode.com/2024/day/21
"""
from aoc.heapdict import heapdict
from collections import defaultdict, namedtuple

State = namedtuple("State", ("numloc", "code", "arrowlocs"))


class KeypadNum:
    def __init__(self, n=2):
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
            (2, 3): "A",
        }
        self.begin_loc = (2, 3)

        self.arrowgrid = {
            # (0, 0): 7, # Not There
            (1, 0): "^",
            (2, 0): "A",
            (0, 1): "<",
            (1, 1): "v",
            (2, 1): ">",
        }
        self.begin_loc_arrow = (2, 0)
        self.n = n
        self.begin_loc_arrows = tuple((2, 0) for _ in range(self.n))

    def search(self, final_code, init_state=None, finish_state=None):
        self.target_code = tuple(list(final_code))
        final_code = tuple(list(final_code))

        if init_state is None:
            init_state = State(self.begin_loc, (), self.begin_loc_arrows)

        dist_to = defaultdict(lambda: 999_999)
        edge_to = defaultdict(list)  # a list of previous states for each state
        open_set = heapdict()
        dist_to[init_state] = 0
        open_set[init_state] = 0
        final_state = None  # Store the final state when we find it

        while len(open_set) > 0:
            (state, length) = open_set.popitem()
            # print(state)
            (numloc, code, arrow_locs) = state
            # print(state)
            if (finish_state is None and code == final_code) or (
                finish_state is not None and state == finish_state
            ):
                final_state = state
                break  # We found our target

            for new_state, cost, name in self.next_states(state):
                if dist_to[new_state] > dist_to[state] + cost:
                    dist_to[new_state] = dist_to[state] + cost
                    edge_to[new_state] = (state, name, cost)

                    if finish_state is not None:
                        open_set[new_state] = dist_to[new_state] + self.h3_build_memo(
                            new_state, finish_state
                        )
                    else:
                        open_set[new_state] = dist_to[new_state] + 0

        if final_state is None:
            return 0, []

        # Reconstruct the path
        path = []
        current_state = final_state
        total_cost = 0
        while current_state in edge_to:
            prev_state, move, cost = edge_to[current_state]
            total_cost += cost
            path.append((prev_state, move))
            current_state = prev_state

        path.reverse()  # Since we built it backwards
        return total_cost, path
        # return len(path), path

    def h1(self, state):
        remaining = len(self.target_code) - len(state.code)
        # Suppose we assume 2 presses minimum per remaining digit.
        # This is naive but guaranteed not to overestimate for large keypads.
        return remaining * 2

    def h2(self, state):
        remaining = len(self.target_code) - len(state.code)
        if remaining == 0:
            return 0

        # Next digit we need to type
        next_digit = self.target_code[len(state.code)]

        # Find next_digit's coordinate on the numeric keypad
        target_coord = None
        for (x, y), val in self.numgrid.items():
            if str(val) == str(next_digit):
                target_coord = (x, y)
                break

        # Current numeric keypad location
        (xn, yn) = state.numloc

        # Manhattan distance as a lower bound
        dist = abs(xn - target_coord[0]) + abs(yn - target_coord[1])

        # For the remaining digits beyond the next one, just multiply by a small factor.
        # We'll say each digit is at least 2 presses (movement + press).
        # So for the next digit, we add 'dist + 1' (1 for pressing),
        # and for the rest we add '2 * (remaining - 1)'
        return (dist + 1) + 2 * (remaining - 1)

    def h3_build_memo(self, new_state, finish_state):
        # print("")
        # print("new   ", new_state)
        # print("final ", finish_state)

        new_arrows = list(reversed(new_state.arrowlocs))
        finish_arrows = list(reversed(finish_state.arrowlocs))
        w = 1
        score = 0
        for i in range(len(new_arrows)):
            # print(i, end=" ")
            (xa, ya) = new_arrows[i]
            (xb, yb) = finish_arrows[i]
            dist = abs(xa - xb) + abs(ya - yb)
            score += dist * w

            w *= 2
        # print("score ", score)
        return score

    def h3(self, state):
        """
        An A* heuristic that:
        - Adds a baseline cost for the remaining digits
        - Sums up distance penalties for each arrow-loc that is not at (2,0)
        - Uses bigger penalty for leftmost and rightmost arrow-locs
        """
        # 1) How many digits remain?
        return 0
        remaining_digits = len(self.target_code) - len(state.code)
        # if remaining_digits <= 0:
        #     return 0

        # 2) Baseline for typing each remaining digit
        #    Assume at least 2 actions per digit (movement + press).
        #    This is usually safe or even conservative.
        baseline = 2 * remaining_digits

        # 3) Arrow-loc penalties
        #    We'll penalize being far from (2,0) because eventually
        #    we need the robot arms back at (2,0) to press the next digit
        #    (or to pass the press command through the chain).

        arrow_penalty = 0
        arrow_count = len(state.arrowlocs)
        w = 2
        terms = []
        # for i, arrow_pos in list(enumerate(state.arrowlocs)):
        for i, arrow_pos in reversed(list(enumerate(state.arrowlocs[1:]))):
            (ax, ay) = arrow_pos
            # Manhattan distance to (2,0)
            dist = abs(ax - 2) + abs(ay - 0)
            # terms.append(w * dist)
            arrow_penalty += w * dist
            w *= 2
        # exit()

        # print(state.arrowlocs, arrow_penalty, list(reversed(terms)))
        # 4) Combine everything
        return baseline + arrow_penalty

    def next_states(self, state):
        numloc = state.numloc
        output = state.code
        arrowlocs = state.arrowlocs

        returns = []
        valid = len(output) <= len(self.target_code) and all(
            a == b for a, b in zip(output, self.target_code)
        )
        if not valid:
            return []

        dirs = {
            "^": (0, -1),
            "v": (0, 1),
            "<": (-1, 0),
            ">": (1, 0),
        }

        i = self.n - 1

        suffix_length = 2  # Number of (2,0) elements required at end
        min_length = 3
        m = Memo()
        used_memo = False
        if (
            len(arrowlocs) >= min_length
            and arrowlocs[-suffix_length:] == ((2, 0),) * suffix_length
        ):
            # Start from longest possible length and work down
            for memo_length in range(len(arrowlocs), min_length - 1, -1):
                memo_key = arrowlocs[-memo_length:]
                if memo_key in m.memo:
                    for locs2, length in m.memo[memo_key]:
                        newarrowlocs = tuple(
                            list(arrowlocs[:-memo_length]) + list(locs2)
                        )
                        new_state = State(numloc, output, newarrowlocs)
                        returns.append((new_state, length, "skip"))
                        # print(f"  Found memo of length {memo_length} --> ", locs2, length)
                    used_memo = True
                    break

        # Try to use memo of 3
        #
        # if len(arrowlocs) >= 3 and arrowlocs[-2:] == ((2,0),) * 2:
        #     m = Memo()
        #     if arrowlocs[-3:] in m.memo:
        #         for (locs2, length) in m.memo[arrowlocs[-3:]]:
        #             newarrowlocs = tuple( list(arrowlocs[:-3]) + list(locs2) )
        #             new_state = State(numloc, output, newarrowlocs)
        #             returns.append(( new_state, length, 'skip' ))
        #             # print("  Found memo --> ", locs2, length)

        # Outermost: can move it
        if not m.flag:
            (x, y) = arrowlocs[i]
            for dir_name, (dx, dy) in dirs.items():
                if (dx + x, dy + y) in self.arrowgrid:
                    new_arrows = tuple(list(arrowlocs[:-1]) + [(dx + x, dy + y)])
                    new_state = State(numloc, output, new_arrows)
                    returns.append((new_state, 1, dir_name))

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
                    if (dx + xx, dy + yy) in self.arrowgrid:
                        # print(f"  decided to move arrowloc {j}")
                        new_arrows = tuple(
                            list(arrowlocs[:j])
                            + [(dx + xx, dy + yy)]
                            + list(arrowlocs[j + 1 :])
                        )
                        new_state = State(numloc, output, new_arrows)
                        returns.append((new_state, 1, "Ac"))
                    else:
                        pass
                        # print(f"  cannot move arrowloc {j} because {dx+xx},{dy+yy} is not in arrowgrid")
                    break
                elif j == -1:
                    # Special Case: j = -1, so move the numpad
                    (xx, yy) = numloc
                    if (dx + xx, dy + yy) in self.numgrid:
                        new_state = State((dx + xx, dy + yy), output, arrowlocs)
                        returns.append((new_state, 1, "Ab"))
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
            if len(new_output) <= len(self.target_code) and all(
                a == b for a, b in zip(new_output, self.target_code)
            ):
                new_state = State(numloc, new_output, arrowlocs)
                returns.append((new_state, 1, "A"))

        # print('--')
        # print('Input state: ', state)
        # for r in returns:
        #     print(r)
        return returns


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Memo(metaclass=Singleton):
    def __init__(self):
        self.memo = defaultdict(list)
        self.flag = False


def parse(filename):
    with open(filename) as file:
        string = file.read().strip()
    return string.split("\n")


def generate_memos(max_length=5):
    m = Memo()

    # Generate all valid location pairs
    kn = KeypadNum(3)
    locations = list(kn.arrowgrid.keys())
    loc_pairs = [
        (loc1, loc2) for loc1 in locations for loc2 in locations if loc1 != loc2
    ]

    # For each memo length from 3 to max_length
    for memo_length in range(2, max_length + 1):
        print("Start generate ", memo_length)
        kn = KeypadNum(memo_length)
        # For each pair of starting locations
        for loc1, loc2 in loc_pairs:
            # Create arrowlocs with one location + (length-1) copies of (2,0)
            arrowlocs1 = tuple([loc1] + list(((2, 0),) * (memo_length - 1)))
            arrowlocs2 = tuple([loc2] + list(((2, 0),) * (memo_length - 1)))

            state1 = State(numloc=(2, 3), code=(), arrowlocs=arrowlocs1)
            state2 = State(numloc=(2, 3), code=(), arrowlocs=arrowlocs2)

            if memo_length == 8:
                print("memosize ", memo_length)
                print("FROM ", state1)
            length, _path = kn.search("", state1, state2)
            # print("")
            if memo_length == 8:
                print("TO   ", state2)
                for p in _path:
                    print(p)
            m.memo[arrowlocs1].append((arrowlocs2, length))
    m.flag = True


class Day21:
    """AoC 2024 Day 21"""

    @staticmethod
    def testme():
        filename = "../inputs/21/input.txt"

        generate_memos(8)
        ## Generate
        # memo = defaultdict(list)
        # m = Memo()
        # kn = KeypadNum(3)
        # for loc1 in kn.arrowgrid.keys():
        #     for loc2 in kn.arrowgrid.keys():
        #         if loc1 == loc2:
        #             continue
        #         arrowlocs1 = tuple( [loc1] + list( ( (2,0), (2, 0) ) ) )
        #         arrowlocs2 = tuple( [loc2] + list( ( (2,0), (2, 0) ) ) )
        #         state1 = State(numloc=(2, 3), code=(), arrowlocs=arrowlocs1)
        #         state2 = State(numloc=(2, 3), code=(), arrowlocs=arrowlocs2)
        #         len, _path = kn.search("", state1, state2)
        #         m.memo[arrowlocs1].append( (arrowlocs2, len) )
        ## Generate

        # for k,v in m.memo.items():
        #     print(k)
        #     for v1 in v:
        #         print("  ", v1)

        # state1 = State(numloc=(2, 3), code=(), arrowlocs=((1, 0), (2, 0), (2, 0) ))
        # state2 = State(numloc=(2, 3), code=(), arrowlocs=((2, 0), (2, 0), (2, 0) ))
        # y, z = kn.search("", state2, state1)
        # print(y)
        # for z1 in z:
        #     print(z1)

        kn = KeypadNum(6)
        ln, path = kn.search("092A")
        for p in path:
            print(p)
        return ln * 92
        # for p in path:
        #     print(p)

    @staticmethod
    def part1or2(filename: str, n: int) -> int:
        codes = parse(filename)
        total = 0
        for code in codes:
            kn = KeypadNum(n)
            (ln, path) = kn.search(code)
            numeric = int(code[:3])
            total += numeric * ln
        return total

    @staticmethod
    def part1(filename: str) -> int:

        # test_state2 = State(numloc=(2, 3), code=(), arrowlocs=((1, 0), (2, 0)))
        # kn = KeypadNum()
        # kn.target_code ='3'
        # kn.next_states(test_state2)
        # return

        generate_memos(9)
        exit()
        print("Start calculate")
        return Day21.part1or2(filename, 10)

    @staticmethod
    def part2(filename: str) -> int:
        pass
