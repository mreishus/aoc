# Day 4: The Ideal Stocking Stuffer

## Approach and Reflections

This was a problem about checking for MD5 hashes beginning with a specified
number of zeros. There is no trick, just iterate, compute, and check. Since
I'm using python and this is a CPU bound problem, using concurrency would not
speed up the solution at all. This is because the GIL lock prevents cpu-bound
parallelism.

## Solutions

- [Python](../python2015/aoc/day04.py)

## Problem Description

[2015 Day 04 on AdventOfCode.com](https://adventofcode.com/2015/day/4)

### Part One

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as
gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
least five zeroes. The input to the MD5 hash is some secret key (your puzzle
input, given below) followed by a number in decimal. To mine AdventCoins, you
must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...)
that produces such a hash.

For example:

- If your secret key is abcdef, the answer is 609043, because the MD5 hash of
  abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest
  such number to do so.
- If your secret key is pqrstuv, the lowest number it combines with to make an
  MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of
  pqrstuv1048970 looks like 000006136ef....

### Part Two

Now find one that starts with six zeroes.
