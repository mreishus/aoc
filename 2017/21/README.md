# Day 21: Fractal Art

## Approach and Reflections

We're given a grid based cellular automata with a couple of complications:

- We need to be able to split the grid into either 2x2 or 3x3 subgrids, apply
  rules and then recombine.
- We need to apply rules from a given ruleset, which includes rotating and
  flipping the input rules if needed.

This was a good exercise to get more familiar with _NumPy_. The most
difficult part was splitting a grid into subgrids.

I imagined stacking up the 2x2 grids in a say, 32 grid by reshaping it:
`matrix.reshape(-1, 2, 2)` should create a 3d matrix of 2x2 matricies, with
the 3rd dimension being whatever it needs to be (`-1` tells numpy to figure
out). Unfortunately, this stacks the first 4 numbers of the first row into
the first layer, instead of taking a 2x2 sub-grid.

I could have written a for loop extracting these using slices, but it didn't
seem very efficient. I searched online for a solution and found
`blockshaped`, which pulls out the subgrids by reshaping to a 4d, then 3d
array.

One other trick that was needed was using numpy arrays as dictionary keys.
They're not hashable, so I needed to use `.tobytes()` to turn them into
something hashable.

Overall, this worked very well. Going forward, I hope to use numpy for advent
of code more often.

## Solutions

- [Python](./python_day21/day21.py)

## Problem Description

[2017 Day 21 on AdventOfCode.com](https://adventofcode.com/2017/day/21)

### Part 1

You find a program trying to generate some art. It uses a strange process that
involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either
on (#) or off (.). The program always begins with this pattern:

```
.#.
..#
###
```

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to
have a size of 3.

Then, the program repeats the following process:

- If the size is evenly divisible by 2, break the pixels up into 2x2 squares,
  and convert each 2x2 square into a 3x3 square by following the corresponding
  enhancement rule.
- Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3
  squares, and convert each 3x3 square into a 4x4 square by following the
  corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains
pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however,
it seems to be missing rules. The artist explains that sometimes, one must
rotate or flip the input pattern to find a match. (Never rotate or flip the
output pattern, though.) Each pattern is written concisely: rows are listed as
single units, ordered top-down, and separated by slashes. For example, the
following rules correspond to the adjacent patterns:

```
../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.
```

When searching for a rule to use, rotate and flip the pattern as necessary.
For example, all of the following patterns match the same rule:

```
.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.
```

Suppose the book contained the following two rules:

```
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
```

As before, the program begins with this pattern:

```
.#.
..#
###
```

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It
divides evenly into a single square; the square matches the second rule, which
produces:

```
#..#
....
....
#..#
```

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is
used. It divides evenly into four squares:

```
#.|.#
..|..
--+--
..|..
#.|.#
```

Each of these squares matches the same rule (../.# => ##./#../...), three of
which require some flipping and rotation to line up with the rule. The output
for the rule is the same in all four cases:

```
##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...
```

Finally, the squares are joined into a new grid:

```
##.##.
#..#..
......
##.##.
#..#..
......
```

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

### Part 2

How many pixels stay on after 18 iterations?
