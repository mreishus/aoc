# Day 24: Air Duct Spelunking

## Approach and Reflections

### Part 1

We're asked to explore a maze, but instead of finding a way out, we need to
visit all points of interest, in whatever order leads to the fewest total
steps.

I implemented a BFS with each state containing both the current coordinates
and the set of important points visited, and defined a goal state as any state
with all points of interest visited.

### Part 2

Now, we have to return to the start position after collecting all points of
interest. I simply changed the final state definition to be
coordinates=start, important points visited = all.

### Conclusion

Thanks to AoC, I can implement a BFS off the top of my head, without using any
references. And I never thought I would say this, but I actually prefer doing
it in Elixir over Python now! Making a function that returns 1 state -> All
possible next states, then flatmapping the frontier to the next frontier with
this, makes so much sense to me.

## Solutions

- [Elixir](../elixir2016/lib/day24.ex)

## Problem Description

[2016 Day 24 on AdventOfCode.com](https://adventofcode.com/2016/day/24)

### Part 1

You've finally met your match; the doors that provide access to the roof are
locked tight, and all of the controls and related electronics are
inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to
interface with some of the exposed wires that have been routed through the
HVAC system. If you can direct it to each of those locations, you should be
able to bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired
and create a map with the relevant locations marked (your puzzle input). 0 is
your current location, from which the cleaning robot embarks; the other
numbers are (in no particular order) the locations the robot needs to visit at
least once each. Walls are marked as #, and open passages are marked as ..
Numbers behave like open passages.

For example, suppose you have a map like the following:

```
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
```

To reach all of the points of interest as quickly as possible, you would have
the robot take the following path:

- 0 to 4 (2 steps)
- 4 to 1 (4 steps; it can't move diagonally)
- 1 to 2 (6 steps)
- 2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route. This
path is the fewest steps (in the above example, a total of 14) required to
start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number
of steps required to visit every non-0 number marked on the map at least once?

### Part 2

Of course, if you leave the cleaning robot somewhere weird, someone is bound
to notice.

What is the fewest number of steps required to start at 0, visit every non-0
number marked on the map at least once, and then return to 0?
