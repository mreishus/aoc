#!/usr/bin/env python
"""
Advent Of Code 2021 Day 21
https://adventofcode.com/2021/day/21
"""
from collections import defaultdict, Counter


class Die:
    def __init__(self):
        self.state = 0
        self.rolls = 0

    def roll(self):
        answer = self.state + 1
        self.state = (self.state + 1) % 100
        self.rolls += 1
        return answer


def wrap(num):
    return ((num - 1) % 10) + 1


class Day21:
    """ AoC 2021 Day 21 """

    @staticmethod
    def part1(filename: str) -> int:
        """ Given a filename, solve 2021 day 21 part 1 """
        data = [9, 3]
        d = Die()

        scores = [0, 0]
        i = 0
        while True:
            delta = d.roll() + d.roll() + d.roll()
            data[i] = wrap(data[i] + delta)
            scores[i] += data[i]
            if scores[i] >= 1000:
                break
            i = (i + 1) % 2
        print(scores)
        j = (i + 1) % 2
        return scores[j] * d.rolls

    @staticmethod
    def part2(filename: str) -> int:
        """ Given a filename, solve 2021 day 21 part 2 """
        roll1 = [3, 4, 5, 4, 5, 6, 5, 6, 7]
        roll2 = [x + 1 for x in roll1]
        roll3 = [x + 2 for x in roll1]
        rolltable = Counter(roll1 + roll2 + roll3)

        i = 0
        WIN = 21

        p1loc = 9
        p1score = 0
        p2loc = 3
        p2score = 0
        state = (p1loc, p1score, p2loc, p2score)
        glob = {state: 1}
        p1_wins = 0
        p2_wins = 0
        while len(glob) > 0:
            new_glob = defaultdict(int)
            for (p1loc, p1score, p2loc, p2score), statefreq in glob.items():
                if i == 0:
                    # Player1 active
                    for roll, rollfreq in rolltable.items():
                        where = wrap(p1loc + roll)
                        howmany = statefreq * rollfreq
                        newscore = p1score + where
                        if newscore >= WIN:
                            p1_wins += howmany
                        else:
                            new_glob[where, newscore, p2loc, p2score] += howmany
                else:
                    # Player2 active
                    for roll, rollfreq in rolltable.items():
                        where = wrap(p2loc + roll)
                        howmany = statefreq * rollfreq
                        newscore = p2score + where
                        if newscore >= WIN:
                            p2_wins += howmany
                        else:
                            new_glob[p1loc, p1score, where, newscore] += howmany

            glob = new_glob
            i = (i + 1) % 2

        return max([p1_wins, p2_wins])
