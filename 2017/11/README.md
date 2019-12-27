# Day 11: Hex Ed

## Approach and Reflections

This was a gentle introduction to hex coordinates. After reading [the
excellent page on redblobgames about hex
grids](https://www.redblobgames.com/grids/hexagons/), I implemented
a straightforward solution using cube coordinates.

## Solutions

- [Elixir](./elixir_day11/lib/elixir_day11.ex) [(test)](./elixir_day11/test/elixir_day11_test.exs)

## Problem Description

[2017 Day 11 on AdventOfCode.com](https://adventofcode.com/2017/day/11)

### Part 1

Crossing the bridge, you've barely reached the other side of the stream when
a program comes up to you, clearly in distress. "It's my child process," she
says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can
be found to the north, northeast, southeast, south, southwest, and northwest:

```
  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
```

You have the path the child process took. Starting where he started, you need
to determine the fewest number of steps required to reach him. (A "step" means
to move from the hex you are in to any adjacent hex.)

For example:

- ne,ne,ne is 3 steps away.
- ne,ne,sw,sw is 0 steps away (back where you started).
- ne,ne,s,s is 2 steps away (se,se).
- se,sw,se,sw,sw is 3 steps away (s,s,sw).

### Part 2

How many steps away is the furthest he ever got from his starting position?
