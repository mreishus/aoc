#!/usr/bin/env python
"""
Advent Of Code 2024 Day 23
https://adventofcode.com/2024/day/23
"""
import re
from typing import List, Set
from collections import defaultdict
from itertools import combinations


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(set)

    def add_edge(self, v1: int, v2: int):
        self.adjacency_list[v1].add(v2)
        self.adjacency_list[v2].add(v1)

    def get_neighbors(self, vertex: int) -> Set[int]:
        return self.adjacency_list[vertex]

def parse(filename):
    with open(filename) as file:
        text = file.read().strip()
    r = []
    for line in text.split("\n"):
        r.append(line.split('-'))
    return r

def is_fully_connected(g, lookup):
    for i, this_g in enumerate(g):
        for j in range(i+1, len(g)):
            this_j = g[j]

            if this_j not in lookup[this_g]:
                return False
    return True

def bron_kerbosch_with_pivot(graph: Graph,
                            potential: Set[int],
                            candidates: Set[int],
                            excluded: Set[int],
                            cliques: List[Set[int]]):
    """
    Implementation of Bron-Kerbosch algorithm with pivot optimization

    Args:
        graph: The input graph
        potential: Current potential clique being built
        candidates: Vertices that could extend the clique
        excluded: Vertices that have been processed
        cliques: List to store all found maximal cliques
    """
    if not candidates and not excluded:
        cliques.append(potential.copy())
        return

    # Choose pivot vertex from candidates ∪ excluded
    pivot_set = candidates.union(excluded)
    if pivot_set:
        pivot = max(pivot_set, key=lambda x: len(graph.get_neighbors(x)))
        pivot_neighbors = graph.get_neighbors(pivot)
        candidates_minus_pivot = candidates.difference(pivot_neighbors)
    else:
        candidates_minus_pivot = candidates

    # Process each candidate vertex
    for vertex in candidates_minus_pivot:
        vertex_neighbors = graph.get_neighbors(vertex)
        new_candidates = candidates.intersection(vertex_neighbors)
        new_excluded = excluded.intersection(vertex_neighbors)

        # Recursive call with updated sets
        bron_kerbosch_with_pivot(
            graph,
            potential.union({vertex}),
            new_candidates,
            new_excluded,
            cliques
        )

        candidates.remove(vertex)
        excluded.add(vertex)

def find_all_cliques(graph: Graph) -> List[Set[int]]:
    """
    Finds all maximal cliques in the given graph

    Args:
        graph: The input graph

    Returns:
        List of all maximal cliques (each clique is a set of vertices)
    """
    vertices = set(graph.adjacency_list.keys())
    cliques = []
    bron_kerbosch_with_pivot(graph, set(), vertices, set(), cliques)
    return cliques



class Day23:
    """AoC 2024 Day 23"""

    @staticmethod
    def part1(filename: str) -> int:
        pairs = parse(filename)
        lookup = defaultdict(list)
        for [x1, x2] in pairs:
            lookup[x1].append(x2)
            lookup[x2].append(x1)

        groups  = combinations( lookup.keys(), 3 )
        ct = 0
        for g in groups:
            (a, b, c) = g
            if a not in lookup[b] or a not in lookup[c]:
                continue
            if b not in lookup[c]:
                continue

            if a[0] != 't' and b[0] != 't' and c[0] != 't':
                continue
            ct += 1
        return ct

    @staticmethod
    def part2(filename: str):
        pairs = parse(filename)
        g = Graph()

        for [x1, x2] in pairs:
            g.add_edge(x1, x2)
        cliques = find_all_cliques(g)
        max_i = 0
        max_set = set()
        for c in cliques:
            if len(c) > max_i:
                max_i = len(c)
                max_set = c
        return ",".join(sorted(max_set))
