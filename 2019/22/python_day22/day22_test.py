#!/usr/bin/env python
from unittest import TestCase, main

from day22 import (
    parse_22,
    simulate,
    shuffle_to_mb,
    mb_to_gen,
    multiple_shuffle_linear,
    multiple_shuffle_simulate,
    part2,
)


class Day22TestCase(TestCase):
    def test_part1_examples(self):
        """ Test the example shuffles given using both simulation and linear equation methods. """
        self.example_helper("../input_036.txt", 10, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])
        self.example_helper("../input_307.txt", 10, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])
        self.example_helper("../input_630.txt", 10, [6, 3, 0, 7, 4, 1, 8, 5, 2, 9])
        self.example_helper("../input_925.txt", 10, [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])

    def example_helper(self, input_file, deck_size, want):
        data = parse_22(input_file)
        # Check that simulating it works
        deck = list(simulate(data, deck_size))
        want = want
        self.assertEqual(deck, want)

        # Check y = mx + b works
        m, b = shuffle_to_mb(data, deck_size)
        deck2 = list(mb_to_gen(m, b, deck_size))
        self.assertEqual(deck2, want)

    def test_part1_simulate(self):
        """ Test the actual part 1 problem using simulation method. """
        data = parse_22("../input.txt")
        deck_size = 10_007
        search_for_value = 2019
        results = simulate(data, deck_size)
        for i, val in enumerate(results):
            if val == search_for_value:
                return i
        return None

    def test_part1_linear(self):
        """ Test the actual part 1 problem using linear equation method. """
        data = parse_22("../input.txt")
        deck_size = 10_007
        search_for_value = 2019
        m, b = shuffle_to_mb(data, deck_size)
        results = mb_to_gen(m, b, deck_size)
        for i, val in enumerate(results):
            if val == search_for_value:
                return i
        return None

    def test_multiple_shuffle_methods(self):
        """ Ensure that shuffling multiple times using linear math and
        matrix multiplication gives the same answer as manually simulating
        the shuffle that many times. """
        data = parse_22("../input.txt")
        deck_size = 10_007
        for num_shuffles in range(1, 15):
            simulate_result = list(
                multiple_shuffle_simulate(data, deck_size, num_shuffles)
            )
            linear_result = multiple_shuffle_linear(data, deck_size, num_shuffles)
            self.assertEqual(simulate_result, linear_result)

    def test_part2(self):
        data = parse_22("../../22/input.txt")
        part2_decksize = 119315717514047
        part2_times = 101741582076661
        p2_answer = part2(data, part2_decksize, part2_times, 2020)
        self.assertEqual(p2_answer, 4893716342290)


if __name__ == "__main__":
    main()
