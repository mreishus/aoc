#!/usr/bin/env python
"""
Advent Of Code 2021 Day 23
https://adventofcode.com/2021/day/23
"""
from collections import namedtuple, defaultdict
import math
import itertools
from heapq import heappush, heappop

# from aoc.heapdict import heapdict

# from heapdict import heapdict

# from copy import deepcopy

State = namedtuple("State", ("podlocs"))
Edge = namedtuple("Edge", ("state", "length"))


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
        ]
        self.must_move = [(3, 1), (5, 1), (7, 1), (9, 1)]
        self.pods = ["A", "A2", "B", "B2", "C", "C2", "D", "D2"]
        self.parse(filename)

    def podi(self, pod):
        return self.pods.index(pod)

    def parse(self, filename):
        grid = defaultdict(lambda: " ")
        x = y = 0
        with open(filename) as f:
            for line in f:
                for char in line.strip("\n"):
                    if char in ["A", "B", "C", "D"]:
                        if self.podlocs[self.podi(char)] != (0, 0):
                            char = char + "2"
                        self.podlocs[self.podi(char)] = (x, y)
                        grid[x, y] = "."
                    else:
                        grid[x, y] = char
                    x += 1
                y += 1
                x = 0
        self.grid = grid

        for i in [0, 2, 4, 6]:
            j = i + 1
            if self.podlocs[i] > self.podlocs[j]:
                self.podlocs[i], self.podlocs[j] = self.podlocs[j], self.podlocs[i]

    def solve(self):
        dist_to = defaultdict(lambda: math.inf)
        edge_to = {}

        state = State(tuple(self.podlocs))
        pq = PriorityQueue()
        dist_to[state] = 0
        pq.add_task(state, 0)
        seen = set()

        while not pq.empty():
            (state, length) = pq.pop_task()
            # print(f"Considering state: {state}")
            if is_winner(state):
                break

            if state in seen:
                continue
            seen.add(state)

            steps = self.possible_edges(state)
            for new_state, length in steps:
                if dist_to[new_state] > dist_to[state] + length:
                    dist_to[new_state] = dist_to[state] + length
                    edge_to[new_state] = state
                    # estimate = 0
                    estimate = self.heuristic_to_goal(new_state)
                    pq.add_task(new_state, dist_to[new_state] + estimate)

        # print("==Done==")
        for k, v in dist_to.items():
            if is_winner(k):
                # return v
                print("Found winner:")
                print(f"{v} {k}")
                win_cost = v
                actual_remaining_costs = {k: 0}
                all_states = [k]
                while k in edge_to:
                    all_states.append(k)
                    # print(edge_to[k])
                    k = edge_to[k]
                    actual_remaining_costs[k] = -1 * (dist_to[k] - win_cost)

                self.animate(list(reversed(all_states)), actual_remaining_costs)
                return v
        return -1

    def animate(self, all_states, actual_remaining_costs):
        for state in all_states:
            self.display(state, actual_remaining_costs)

    def display(self, state, actual_remaining_costs):
        podlocs = state.podlocs
        for y in range(5):
            for x in range(13):
                if (x, y) in [podlocs[0], podlocs[1]]:
                    print("A", end="")
                elif (x, y) in [podlocs[2], podlocs[3]]:
                    print("B", end="")
                elif (x, y) in [podlocs[4], podlocs[5]]:
                    print("C", end="")
                elif (x, y) in [podlocs[6], podlocs[7]]:
                    print("D", end="")
                else:
                    print(self.grid[x, y], end="")
            print("")
        estimate = self.heuristic_to_goal_force(state)
        print(f"Estimate energy remaining: {estimate}")
        print(f"Actual energy remaining: {actual_remaining_costs[state]}")
        print("")

    def heuristic_to_goal_force(self, state):
        podlocs = list(state.podlocs)
        ideal = [(3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3)]
        cost = 0

        def get_dist(x1, y1, x2, y2):
            return abs(x2 - x1) + abs(y2 - y1)

        chunk_num = 0
        for actual_pair, ideal_pair in zip(chunks(podlocs, 2), chunks(ideal, 2)):
            [(ax1, ay1), (ax2, ay2)] = actual_pair
            [(ix1, iy1), (ix2, iy2)] = ideal_pair
            normal_dist = get_dist(ax1, ay1, ix1, iy1) + get_dist(ax2, ay2, ix2, iy2)
            swap_dist = get_dist(ax1, ay1, ix2, iy2) + get_dist(ax2, ay2, ix1, iy1)
            dist = min(normal_dist, swap_dist)
            cost += dist * get_energy(chunk_num * 2)
            chunk_num += 1
        # for i in range(len(ideal)):
        #     (x1, y1) = podlocs[i]
        #     (x2, y2) = ideal[i]
        #     dist = abs(x2 - x1) + abs(y2 - y1)
        #     cost += dist * get_energy(i)
        return cost

    def heuristic_to_goal(self, state):
        return self.heuristic_to_goal_force(state)
        return 0
        podlocs = state.podlocs
        ideal = ((3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3))
        cost = 0
        for i in range(len(ideal)):
            (x1, y1) = podlocs[i]
            (x2, y2) = ideal[i]
            dist = abs(x2 - x1) + abs(y2 - y1)
            cost += dist * get_energy(i)
        return cost

    def possible_edges(self, state):
        podlocs = state.podlocs

        # self.display()

        # Check if someone must move
        free_to_move = list(range(len(podlocs)))
        for i in range(len(podlocs)):
            if podlocs[i] in self.must_move:
                free_to_move = [i]

        edges = []
        for pod in free_to_move:
            loc = podlocs[pod]
            # print(f"{pod} {loc}")
            for x, y in get_neighbors(loc):
                if self.grid[x, y] == "#":
                    continue
                if (x, y) in podlocs:
                    continue

                if loc[1] == 1 and y == 2:
                    # Case: Moving down to room
                    # Only move into my rooms
                    if pod in [0, 1]:
                        if x != 3:
                            continue
                        other = podlocs[2:]
                        if (x, y + 1) in other:
                            continue
                    elif pod in [2, 3]:
                        if x != 5:
                            continue
                        other = podlocs[0:2] + podlocs[4:]
                        if (x, y + 1) in other:
                            continue
                    elif pod in [4, 5]:
                        if x != 7:
                            continue
                        other = podlocs[0:4] + podlocs[6:]
                        if (x, y + 1) in other:
                            continue
                    elif pod in [6, 7]:
                        if x != 9:
                            continue
                        other = podlocs[6:7]
                        if (x, y + 1) in other:
                            continue

                    # ideal = ((3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3))
                    # print("Moving down to room")

                newlocs = list(podlocs)
                newlocs[pod] = (x, y)

                # Try to make robot pairs fungible
                for i in [0, 2, 4, 6]:
                    j = i + 1
                    if newlocs[i] > newlocs[j]:
                        newlocs[i], newlocs[j] = newlocs[j], newlocs[i]

                new_state = State(tuple(newlocs))
                energy = get_energy(pod)
                edges.append(Edge(new_state, energy))

        return edges


def get_energy(pod):
    a = 0
    a2 = 1
    b = 2
    b2 = 3
    c = 4
    c2 = 5
    d = 6
    d2 = 7
    if pod == a or pod == a2:
        return 1
    if pod == b or pod == b2:
        return 10
    if pod == c or pod == c2:
        return 100
    if pod == d or pod == d2:
        return 1000
    raise ValueError


def get_neighbors(loc):
    x, y = loc
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def is_winner(state: State):
    a = 0
    a2 = 1
    b = 2
    b2 = 3
    c = 4
    c2 = 5
    d = 6
    d2 = 7
    is_a = (state.podlocs[a] == (3, 2) and state.podlocs[a2] == (3, 3)) or (
        state.podlocs[a] == (3, 3) and state.podlocs[a2] == (3, 2)
    )
    is_b = (state.podlocs[b] == (5, 2) and state.podlocs[b2] == (5, 3)) or (
        state.podlocs[b] == (5, 3) and state.podlocs[b2] == (5, 2)
    )
    is_c = (state.podlocs[c] == (7, 2) and state.podlocs[c2] == (7, 3)) or (
        state.podlocs[c] == (7, 3) and state.podlocs[c2] == (7, 2)
    )
    is_d = (state.podlocs[d] == (9, 2) and state.podlocs[d2] == (9, 3)) or (
        state.podlocs[d] == (9, 3) and state.podlocs[d2] == (9, 2)
    )
    return is_a and is_b and is_c and is_d


class Day23:
    """ AoC 2021 Day 23 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 1 """
        m = Maze(filename)
        return m.solve()
        # Too Low:  (You guessed 16051.)
        # Too High: (You guessed 16091.)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 2 """
        return -1


if __name__ == "__main__":
    print(Day23.part1("/home/p22/h21/dev/aoc/2021/inputs/23/input.txt"))
