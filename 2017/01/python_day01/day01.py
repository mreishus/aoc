#!/usr/bin/env python3
"""
Advent of Code 2017 Day 01.
"""


class Day01:
    """Main module for solving Day01."""

    @staticmethod
    def rotate(input_str: str, num: int) -> str:
        """Rotate a string by `num` characters."""
        return input_str[num:] + input_str[:num]

    @staticmethod
    def part1(input_str: str) -> int:
        return Day01.captcha(input_str, 1)

    @staticmethod
    def part2(input_str: str) -> int:
        rotate_amount = int(len(input_str) / 2)
        return Day01.captcha(input_str, rotate_amount)

    @staticmethod
    def captcha(input_str: str, rotate_amount: int) -> int:
        rotated = Day01.rotate(input_str, rotate_amount)
        count = 0
        for str1, str2 in zip(input_str, rotated):
            if str1 == str2:
                count += int(str1)
        return count


if __name__ == "__main__":
    print("Hello from main")
    with open("../input.txt", "r") as file:
        data = file.read().replace("\n", "")
    print("part 1:")
    print(Day01.part1(data))
    print("part 2:")
    print(Day01.part2(data))
    # print("rotate:")
    # r = Day01.rotate("1234", 5)
    # print(r)
