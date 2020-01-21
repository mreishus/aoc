# Day 19: An Elephant Named Joseph

## Approach and Reflections

We're given the Josephus problem for Part 1. Part 2 is a twist on the
problem: each elf/soldier kills the person across from them in the circle
instead of the neighbor.

For Part 1, I was already familiar with [Numberphile's Video on the Josephus
Problem](https://www.youtube.com/watch?v=uCsD3ZGzMgE), so I simply implemented
the mathematical closed form solution.

For Part 2, I followed the same approach they did in the video. I wrote
a quick python simulation that only worked on small numbers, and wrote out the
solutions for n = 1 to 100 and looked for a pattern. Then I implemented an
equation fitting that pattern in my elixir program.

## Solutions

- [Elixir](../elixir2016/lib/day19.ex)

## Problem Description

[2016 Day 19 on AdventOfCode.com](https://adventofcode.com/2016/day/19)

### Part 1

The Elves contact you over a highly secure emergency channel. Back at the North
Pole, the Elves are busy misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with
position 1. Then, starting with the first Elf, they take turns stealing all the
presents from the Elf to their left. An Elf with no presents is removed from
the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

```
  1
5   2
 4 3
```

- Elf 1 takes Elf 2's present.
- Elf 2 has no presents and is skipped.
- Elf 3 takes Elf 4's present.
- Elf 4 has no presents and is also skipped.
- Elf 5 takes Elf 1's two presents.
- Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
- Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all the
presents.

With the number of Elves given in your puzzle input, which Elf gets all the
presents?

### Part 2

Realizing the folly of their present-exchange rules, the Elves agree to instead
steal presents from the Elf directly across the circle. If two Elves are across
the circle, the one on the left (from the perspective of the stealer) is stolen
from. The other rules remain unchanged: Elves with no presents are removed from
the circle entirely, and the other elves move in slightly to keep the circle
evenly spaced.

For example, with five Elves (again numbered 1 to 5):

- The Elves sit in a circle; Elf 1 goes first:

```
      1
    5   2
     4 3
```

- Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one
  to the left. Elf 3 leaves the circle, and the rest of the Elves move in:

```
      1           1
    5   2  -->  5   2
     4 -          4
```

- Elf 2 steals from the Elf directly across the circle, Elf 5:

```
      1         1
    -   2  -->     2
      4         4
```

- Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

```
     -          2
        2  -->
     4          4
```

- Finally, Elf 2 steals from Elf 4:

```
     2
        -->  2
     -
```

So, with five Elves, the Elf that sits starting in position 2 gets all the
presents.

With the number of Elves given in your puzzle input, which Elf now gets all the
presents?
