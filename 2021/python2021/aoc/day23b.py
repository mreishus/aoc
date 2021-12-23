#!/usr/bin/env python
"""
Advent Of Code 2021 Day 23
https://adventofcode.com/2021/day/23
"""
from collections import namedtuple, defaultdict, deque
import math
import itertools
from itertools import permutations
from heapq import heappush, heappop

State = namedtuple("State", ("podlocs", "moving", "moved_once", "moved_twice"))
Edge = namedtuple("Edge", ("state", "length"))

ideal = [
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
    (9, 2),
    (9, 3),
    (9, 4),
    (9, 5),
]


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


class PriorityQueue:
    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = "<removed-task>"  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority=0):
        "Add a new task or update the priority of an existing task"
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        "Remove and return the lowest priority task. Raise KeyError if empty."
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, priority
        raise KeyError("pop from an empty priority queue")

    def empty(self):
        return len(self.pq) == 0


class SimpleMaze:
    def __init__(self, grid):
        self.grid = grid
        self.cache = {}

    def path_distance(self, coord1, coord2):
        if (coord1, coord2) in self.cache:
            return self.cache[(coord1, coord2)]

        q = deque([(coord1, 0)])
        seen = set()

        while len(q) > 0:
            loc, steps = q.popleft()

            if loc == coord2:
                self.cache[(coord1, coord2)] = steps
                self.cache[(coord2, coord1)] = steps
                return steps
            seen.add(loc)

            for next_loc in get_neighbors(loc):
                if self.grid[next_loc] == "#":
                    continue
                if next_loc in seen:
                    continue
                q.append((next_loc, steps + 1))
        return -1


class Maze:
    def __init__(self, filename):
        self.grid = {}
        self.podlocs = [
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ]
        self.must_move = [(3, 1), (5, 1), (7, 1), (9, 1)]
        self.pods = [
            "A",
            "A2",
            "A3",
            "A4",
            "B",
            "B2",
            "B3",
            "B4",
            "C",
            "C2",
            "C3",
            "C4",
            "D",
            "D2",
            "D3",
            "D4",
        ]
        self.parse(filename)
        self.simple_maze = SimpleMaze(self.grid)

    def maze_distance(self, coord1, coord2):
        # return self.simple_maze.path_distance((3, 4), (5, 2))
        return self.simple_maze.path_distance(coord1, coord2)

    def podi(self, pod):
        return self.pods.index(pod)

    def parse(self, filename):
        grid = defaultdict(lambda: " ")
        x = y = 0
        with open(filename) as f:
            for line in f:
                for char in line.strip("\n"):
                    if char in ["A", "B", "C", "D"]:
                        orig_char = char
                        if self.podlocs[self.podi(char)] != (0, 0):
                            char = char + "2"
                            if self.podlocs[self.podi(char)] != (0, 0):
                                char = orig_char + "3"
                                if self.podlocs[self.podi(char)] != (0, 0):
                                    char = orig_char + "4"
                        self.podlocs[self.podi(char)] = (x, y)
                        grid[x, y] = "."
                    else:
                        grid[x, y] = char
                    x += 1
                y += 1
                x = 0
        self.grid = grid

        for i in [0, 4, 8, 12]:
            self.podlocs[i : i + 4] = sorted(self.podlocs[i : i + 4])

    def solve(self):
        dist_to = defaultdict(lambda: 999_999_999_999)
        edge_to = {}

        state = State(tuple(self.podlocs), tuple(), frozenset(), frozenset())

        pq = PriorityQueue()
        dist_to[state] = 0
        pq.add_task(state, 0)
        seen = set()

        max_q_len = 0
        while not pq.empty():
            (state, length) = pq.pop_task()
            if len(pq.pq) % 1000 == 0:
                max_q_len = max(max_q_len, len(pq.pq))
                print(len(pq.pq))
            if False and len(pq.pq) > 8000:
                i = 0
                for cost, counter, state in pq.pq:
                    if state == "<removed-task>":
                        continue
                    print(state, cost, counter)
                    print(f"i={i} unsolv={self.is_state_unsolvable(state)}")
                    self.display(state, {})
                    i += 1
                exit()

            # print(f"Considering state: {state}")
            if is_winner(state):
                break

            if state in seen:
                continue
            seen.add(state)

            # print("---> Looking for new states")
            steps = self.possible_edges(state)
            for new_state, length in steps:
                # self.display(new_state, {})
                if dist_to[new_state] > dist_to[state] + length:
                    dist_to[new_state] = dist_to[state] + length
                    edge_to[new_state] = state
                    # estimate = 0
                    estimate = self.heuristic_to_goal(new_state)
                    pq.add_task(new_state, dist_to[new_state] + estimate)
            # exit()

        # print("==Done==")
        for k, v in dist_to.items():
            if is_winner(k):
                # return v
                win_cost = v
                actual_remaining_costs = {k: 0}
                all_states = [k]
                while k in edge_to:
                    all_states.append(k)
                    # print(edge_to[k])
                    k = edge_to[k]
                    actual_remaining_costs[k] = -1 * (dist_to[k] - win_cost)

                self.animate(list(reversed(all_states)), actual_remaining_costs)
                print(f"Max Q length: {max_q_len}")
                print("Found winner:")
                print(f"{v} {k}")
                return v
        return -1

    def animate(self, all_states, actual_remaining_costs):
        for state in all_states:
            self.display(state, actual_remaining_costs)

    def display(self, state, actual_remaining_costs):
        podlocs = state.podlocs
        for y in range(7):
            for x in range(13):
                if (x, y) in [podlocs[0], podlocs[1], podlocs[2], podlocs[3]]:
                    print("A", end="")
                elif (x, y) in [podlocs[4], podlocs[5], podlocs[6], podlocs[7]]:
                    print("B", end="")
                elif (x, y) in [podlocs[8], podlocs[9], podlocs[10], podlocs[11]]:
                    print("C", end="")
                elif (x, y) in [podlocs[12], podlocs[13], podlocs[14], podlocs[15]]:
                    print("D", end="")
                else:
                    print(self.grid[x, y], end="")
            print("")
        estimate = self.heuristic_to_goal(state)
        print(f"Estimate energy remaining: {estimate}")
        if state in actual_remaining_costs:
            print(f"Actual energy remaining: {actual_remaining_costs[state]}")
        print(f"Moving: {state.moving}")
        print(f"Moved once: {state.moved_once}")
        print(f"Moved twice: {state.moved_twice}")
        # print(f"Is unsolvable: {self.is_state_unsolvable(state)}")
        print("")

    def is_state_unsolvable(self, state):
        podlocs = state.podlocs

        chunk_num = 0
        for actual_pair, ideal_pair in zip(chunks(podlocs, 4), chunks(ideal, 4)):
            ## Moved twice but not in "My Room": Unsolvable
            for pair in actual_pair:
                if (
                    pair in state.moved_twice
                    and pair != state.moving
                    and pair != ideal_pair[0]
                    and pair != ideal_pair[1]
                    and pair != ideal_pair[2]
                    and pair != ideal_pair[3]
                ):
                    return True

            ## Moved once, but in "someone else's room": Unsolvable
            for pair in actual_pair:
                if (
                    pair[1] > 1
                    and pair in state.moved_once
                    and pair != state.moving
                    and pair != ideal_pair[0]
                    and pair != ideal_pair[1]
                    and pair != ideal_pair[2]
                    and pair != ideal_pair[3]
                ):
                    return True

            ## Moved once or twice, in my room, not at the bottom
            ## Spaces below me are empty: Unsolvable, I should have kept
            ## moving to bottom space.
            for pair in actual_pair:
                if (
                    (pair in state.moved_once or pair in state.moved_twice)
                    and pair != state.moving
                    and pair in ideal_pair
                    and pair[1] < 5
                ):

                    for y in range(pair[1] + 1, 6):
                        if (pair[0], y) not in actual_pair:
                            # self.display(state, {})
                            # print(f"--> {pair} <--")
                            # print(f"Check {pair[0]}, {y} FAILED")
                            return True

            # all_js = permutations([0, 1, 2, 3], 4)
            # for js in all_js:
            #     for i, j in enumerate(js):
            #         me, him = actual_pair[i], actual_pair[j]
            #         if (
            #             (me in state.moved_once or me in state.moved_twice)
            #             and me != state.moving
            #             and me[1] == 2
            #             and him != ideal_pair[0]
            #             and him != ideal_pair[1]
            #             and him != ideal_pair[2]
            #             and him != ideal_pair[3]
            #         ):
            #             return True

            chunk_num += 1

        return False

    def heuristic_to_goal(self, state):
        podlocs = list(state.podlocs)
        cost = 0

        def get_dist(coord1, coord2):
            (x1, y1) = coord1
            (x2, y2) = coord2
            return self.maze_distance(coord1, coord2)
            # return abs(x2 - x1) + abs(y2 - y1)
            # return abs(x2 - x1) + abs(y2 - y1)

        chunk_num = 0
        for actual_pair, ideal_pair in zip(chunks(podlocs, 4), chunks(ideal, 4)):
            all_js = permutations([0, 1, 2, 3], 4)
            all_dists = []
            for js in all_js:
                dist = 0
                for i, j in enumerate(js):
                    dist += get_dist(actual_pair[i], ideal_pair[j])
                all_dists.append(dist)
            # print(actual_pair)
            # print(ideal_pair)
            # exit()
            # [(ax1, ay1), (ax2, ay2)] = actual_pair
            # [(ix1, iy1), (ix2, iy2)] = ideal_pair

            # normal_dist = get_dist(ax1, ay1, ix1, iy1) + get_dist(ax2, ay2, ix2, iy2)
            # swap_dist = get_dist(ax1, ay1, ix2, iy2) + get_dist(ax2, ay2, ix1, iy1)

            dist = min(all_dists)
            cost += dist * get_energy(chunk_num * 4)

            chunk_num += 1
        return cost

    def possible_edges(self, state):
        (podlocs, moving, moved_once, moved_twice) = state

        # Check if someone must move
        free_to_move = list(range(len(podlocs)))
        for i in range(len(podlocs)):
            if podlocs[i] in self.must_move:
                free_to_move = [i]

        edges = []
        for pod in free_to_move:
            loc = podlocs[pod]
            # print(f"{pod} {loc}")
            if loc in moved_twice and moving != loc:
                continue
            for x, y in get_neighbors(loc):
                if self.grid[x, y] == "#":
                    continue
                if (x, y) in podlocs:
                    continue

                if loc[1] == 1 and y == 2:
                    # Case: Moving down to room
                    # Only move into my rooms
                    # + Don't move into my room when wrong pods are in it
                    if pod in [0, 1, 2, 3]:
                        if x != 3:
                            continue
                        other = podlocs[4:]
                        if (
                            (x, y + 1) in other
                            or (x, y + 2) in other
                            or (x, y + 3) in other
                        ):
                            continue
                    elif pod in [4, 5, 6, 7]:
                        if x != 5:
                            continue
                        other = podlocs[0:4] + podlocs[8:]
                        if (
                            (x, y + 1) in other
                            or (x, y + 2) in other
                            or (x, y + 3) in other
                        ):
                            continue
                    elif pod in [8, 9, 10, 11]:
                        if x != 7:
                            continue
                        other = podlocs[0:8] + podlocs[12:]
                        if (
                            (x, y + 1) in other
                            or (x, y + 2) in other
                            or (x, y + 3) in other
                        ):
                            continue
                    elif pod in [12, 13, 14, 15]:
                        if x != 9:
                            continue
                        other = podlocs[:12]
                        if (
                            (x, y + 1) in other
                            or (x, y + 2) in other
                            or (x, y + 3) in other
                        ):
                            continue

                newlocs = list(podlocs)
                new_moved_once = list(moved_once)
                new_moved_twice = list(moved_twice)

                (old_x, old_y) = newlocs[pod]
                newlocs[pod] = (x, y)

                # POD moving from old_x,old_y -> x,y

                if loc in new_moved_once:
                    new_moved_once.remove(loc)
                    new_moved_once.append((x, y))
                elif loc in new_moved_twice:
                    new_moved_twice.remove(loc)
                    new_moved_twice.append((x, y))
                # print(
                #     f"{pod} Is moving from {old_x},{old_y} to {x},{y}. Current moving={moving}"
                # )

                track_extra_rules = True  # Slower but gets correct p1 answer
                # track_extra_rules = False  # Faster but gets incorrect p1 answer

                if track_extra_rules and len(moving) and moving != loc:
                    # moving = Last thing that was moving
                    # old_x, old_y = New mover's original location
                    # x, y = New mover's new location

                    # print(
                    #     f"Something else started moving. moving={moving} myprev={(old_x, old_y)}"
                    # )

                    # Moving is now STOPPING.
                    if moving in new_moved_once:
                        new_moved_once.remove(moving)
                        new_moved_twice.append(moving)
                    else:
                        if moving[1] > 1:
                            # Stopping moving in a room: Auto-promote to moved twice
                            new_moved_twice.append(moving)
                        else:
                            new_moved_once.append(moving)
                newmoving = (x, y)

                # Try to make robot pairs fungible
                for i in [0, 4, 8, 12]:
                    newlocs[i : i + 4] = sorted(newlocs[i : i + 4])

                new_state = State(
                    tuple(newlocs),
                    newmoving,
                    frozenset(new_moved_once),
                    frozenset(new_moved_twice),
                )

                energy = get_energy(pod)
                if not self.is_state_unsolvable(new_state):
                    edges.append(Edge(new_state, energy))

        return edges


def get_energy(pod):
    if 0 <= pod and pod <= 3:
        return 1
    if 4 <= pod and pod <= 7:
        return 10
    if 8 <= pod and pod <= 11:
        return 100
    if 12 <= pod and pod <= 15:
        return 1000
    raise ValueError


def get_neighbors(loc):
    x, y = loc
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def is_winner(state: State):
    # return sorted(state.podlocs) == ideal
    As = sorted(
        [state.podlocs[0], state.podlocs[1], state.podlocs[2], state.podlocs[3],]
    )
    if As != [(3, 2), (3, 3), (3, 4), (3, 5)]:
        return False

    Bs = sorted(
        [state.podlocs[4], state.podlocs[5], state.podlocs[6], state.podlocs[7],]
    )
    if Bs != [(5, 2), (5, 3), (5, 4), (5, 5)]:
        return False

    Cs = sorted(
        [state.podlocs[8], state.podlocs[9], state.podlocs[10], state.podlocs[11],]
    )
    if Cs != [(7, 2), (7, 3), (7, 4), (7, 5)]:
        return False

    Ds = sorted(
        [state.podlocs[12], state.podlocs[13], state.podlocs[14], state.podlocs[15],]
    )
    if Ds != [(9, 2), (9, 3), (9, 4), (9, 5)]:
        return False
    return True


class Day23:
    """ AoC 2021 Day 23 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 1 """
        m = Maze(filename)
        return m.solve()

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 2 """
        return -1


if __name__ == "__main__":
    print(Day23.part1("../inputs/23/input_b.txt"))
