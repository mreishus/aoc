#!/usr/bin/env python
"""
Advent Of Code 2021 Day 23
https://adventofcode.com/2021/day/23
"""
from collections import namedtuple, defaultdict, deque
import math
import itertools
from heapq import heappush, heappop

State = namedtuple("State", ("podlocs", "moving", "moved_once", "moved_twice"))
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
        ]
        self.must_move = [(3, 1), (5, 1), (7, 1), (9, 1)]
        self.pods = ["A", "A2", "B", "B2", "C", "C2", "D", "D2"]
        self.parse(filename)
        self.simple_maze = SimpleMaze(self.grid)

    def maze_distance(self, coord1, coord2):
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
        dist_to = defaultdict(lambda: 999_999_999_999)
        edge_to = {}

        state = State(tuple(self.podlocs), tuple(), frozenset(), frozenset())
        pq = PriorityQueue()
        dist_to[state] = 0
        pq.add_task(state, 0)
        seen = set()

        while not pq.empty():
            (state, length) = pq.pop_task()
            if len(pq.pq) % 1000 == 0:
                print(len(pq.pq))
            # if len(pq.pq) > 40000:
            #     i = 0
            #     for cost, counter, state in pq.pq:
            #         if state == "<removed-task>":
            #             continue
            #         print(state, cost, counter)
            #         print(f"i={i} unsolv={self.is_state_unsolvable(state)}")
            #         self.display(state, {})
            #         i += 1
            #     exit()

            # print(f"Considering state: {state}")
            if is_winner(state):
                break

            # if state in seen:
            #     continue
            # seen.add(state)

            # print("---> Looking for new states")
            steps = self.possible_edges(state)
            for new_state, length in steps:
                # print(new_state)
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
        ideal = [(3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3)]

        chunk_num = 0
        for actual_pair, ideal_pair in zip(chunks(podlocs, 2), chunks(ideal, 2)):
            ## Moved twice but not in "My Room": Unsolvable
            for pair in actual_pair:
                if (
                    pair in state.moved_twice
                    and pair != state.moving
                    and pair != ideal_pair[0]
                    and pair != ideal_pair[1]
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
                ):
                    return True

            ## Moved one or twice, in top slot of "my room", but bottom slot of my room is not occupied
            for i0, i1 in [(0, 1), (1, 0)]:
                me, him = actual_pair[i0], actual_pair[i1]
                if (
                    (me in state.moved_once or me in state.moved_twice)
                    and me != state.moving
                    and me[1] == 2
                    and him != ideal_pair[0]
                    and him != ideal_pair[1]
                ):
                    return True

            chunk_num += 1

        return False

    def heuristic_to_goal(self, state):
        podlocs = list(state.podlocs)
        ideal = [(3, 2), (3, 3), (5, 2), (5, 3), (7, 2), (7, 3), (9, 2), (9, 3)]
        cost = 0

        def get_dist(coord1, coord2):
            return self.maze_distance(coord1, coord2)

        chunk_num = 0
        for actual_pair, ideal_pair in zip(chunks(podlocs, 2), chunks(ideal, 2)):
            [(ax1, ay1), (ax2, ay2)] = actual_pair
            [(ix1, iy1), (ix2, iy2)] = ideal_pair

            normal_dist = get_dist((ax1, ay1), (ix1, iy1)) + get_dist(
                (ax2, ay2), (ix2, iy2)
            )
            swap_dist = get_dist((ax1, ay1), (ix2, iy2)) + get_dist(
                (ax2, ay2), (ix1, iy1)
            )

            dist = min(normal_dist, swap_dist)
            cost += dist * get_energy(chunk_num * 2)

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
                # track_extra_rules = False # Faster but gets incorrect p1 answer

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
                for i in [0, 2, 4, 6]:
                    j = i + 1
                    if newlocs[i] > newlocs[j]:
                        newlocs[i], newlocs[j] = newlocs[j], newlocs[i]

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

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 23 part 2 """
        return -1


if __name__ == "__main__":
    print(Day23.part1("../inputs/23/input.txt"))
