# Day 4: Secure Container

## Approach and Reflections

The problem was to check a range of numbers to see if they satisfy a list of
password criteria. When I went to solve the problem quickly, I did not read
the criteria correctly and made an incorrect assumption, leading to an invalid
solution. When I saw that `111122` passed part two, I incorrectly assumed
`111123` would also pass, and wrote code looking for odd groupings of
digits: Fail if there is a group of 3 or 5 consecutive digits, but pass if 2,
4, or 6. [I wasn't the only
one.](https://old.reddit.com/r/adventofcode/comments/e5uatc/the_two_adjacent_matching_digits_are_not_part_of/)
This was a good reminder of how important it is to closely examine the
requirements when implementing any solution.

For part 2, I first went with a run-length encoding approach, but I changed to
a simple hash counter after realizing the monotonic digit requirement made
detecting a group of 2 easier.

## Solutions

- [Python](./python_day04/day04.py) [(test)](./python_day04/day04_test.py)

## Problem Description

[2019 Day 04 on AdventOfCode.com](https://adventofcode.com/2019/day/4)

### Part 1

You arrive at the Venus fuel depot only to discover it's protected by
a password. The Elves had written the password on a sticky note, but someone
threw it out.

However, they do remember a few key facts about the password:

- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever increase
  or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

- 111111 meets these criteria (double 11, never decreases).
- 223450 does not meet these criteria (decreasing pair of digits 50).
- 123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

### Part 2

An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

- 112233 meets these criteria because the digits never decrease and all
  repeated digits are exactly two digits long.
- 123444 no longer meets the criteria (the repeated 44 is part of a larger
  group of 444).
- 111122 meets the criteria (even though 1 is repeated more than twice, it
  still contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?
