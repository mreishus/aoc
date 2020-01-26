#!/usr/bin/env python
"""
Advent Of Code 2015 Day 9
https://adventofcode.com/2015/day/9
"""

from typing import Dict, List, Set, Tuple
import re
from itertools import permutations
from aoc.parsers import all_lines

# example line: "London to Dublin = 464"
PARSER = re.compile(r"(\w+) to (\w+) = (\d+)")

def parse(lines: List[str]) -> Tuple[Dict[Tuple[str, str], int], Set[str]]:
    """
    Input: A list of lines.
    Output: A tuple containing (distances, cities).
        distances: A dictionary with
            Keys: Tuples containing strings like ("Dallas", "New York")
            Values: Integer representing the distance between those cities
        cities: A set containing strings, listing all cities
    """
    distances = {}
    cities = set()
    # example line: "London to Dublin = 464"
    for line in lines:
        match = re.search(PARSER, line)
        if not bool(match):
            raise ValueError("Can't parse line")
        (city1, city2, dist) = match.groups()
        dist = int(dist)
        distances[(city1, city2)] = dist
        distances[(city2, city1)] = dist
        cities.add(city1)
        cities.add(city2)
    return distances, cities

def shortest_distance(distances: Dict[Tuple[str, str], int], cities: Set[str]):
    perms = permutations(list(cities))
    winner = min(perms, key=lambda path: path_distance(list(path), distances))
    return path_distance(winner, distances)

def longest_distance(distances: Dict[Tuple[str, str], int], cities: Set[str]):
    perms = permutations(list(cities))
    winner = max(perms, key=lambda path: path_distance(list(path), distances))
    return path_distance(winner, distances)

def path_distance(path: List[str], distances: Dict[Tuple[str, str], int]):
    distance = 0
    for (city1, city2) in zip(path, path[1:]):
        distance += distances[(city1, city2)]
    return distance

class Day09:
    """ AoC 2015 Day 09 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2015 day 09 part 1 """
        distances, cities = parse(all_lines(filename))
        return shortest_distance(distances, cities)

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2015 day 09 part 2 """
        distances, cities = parse(all_lines(filename))
        return longest_distance(distances, cities)
