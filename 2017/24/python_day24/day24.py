#!/usr/bin/env python
from typing import Tuple, List


def parse(filename: str) -> List[Tuple[int, int]]:
    segments = []
    with open(filename) as file:
        for line in file:
            left, right = line.split("/")
            segment = (int(left), int(right))
            segments.append(segment)
    return segments


def find_bridges(
    previously_built: List[Tuple[int, int]],
    segments: List[Tuple[int, int]],
    starting_port: int,
) -> List[List[Tuple[int, int]]]:
    """ Recursively build up a list of bridges.
    A bridge is a list of segments that can connect, like:
    [ (0, 2), (2, 3), (5, 3), (10, 5) ]
    Note that left doesn't have to match with right, any segment can be
    flipped.
    """
    results = [previously_built]
    matching = [
        (l, r) for (l, r) in segments if l == starting_port or r == starting_port
    ]
    for match in matching:
        if match[0] == starting_port:
            ending_port = match[1]
        elif match[1] == starting_port:
            ending_port = match[0]
        else:
            raise ValueError("ports don't make sense")
        this_bridge = previously_built + [match]
        remaining_bridges = [b for b in segments if b != match]
        for r in find_bridges(this_bridge, remaining_bridges, ending_port):
            results.append(r)
    return results


def strength(bridge: List[Tuple[int, int]]) -> int:
    stren = 0
    for (l, r) in bridge:
        stren += l + r
    return stren


if __name__ == "__main__":
    segments = parse("../input.txt")
    bridges = find_bridges([], segments, 0)
    strongest = max(bridges, key=strength)
    longest = max(bridges, key=lambda b: (len(b), strength(b)))
    print("Part1: strength of the strongest bridge: ")
    print(strength(strongest))
    print("Part2: strength of the longest bridge, with strength as tiebreaker:")
    print(strength(longest))
