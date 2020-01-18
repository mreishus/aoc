# Day 13: A Maze of Twisty Little Cubicles

## Approach and Reflections

We're given a maze that's revealed through use of an algorithm. Plug X, Y into
a special formula that uses some bitwise math, and that reveals if that square
is a wall or not.

Then we're asked to find the shortest distance between 1,1 and 31,39, and for
part 2, how many squares can be reached in 50 steps or fewer.

This was a straightforward implementation of BFS. After implementing BFS in
elixir a few times, I'm seeing more of the benefits of functional programming.
My BFS from two days ago was abstract enough that it could be mostly reused
with only minor changes.

One odd part was "counting the number of 1s in the binary representation of an
integer." I had to google for a fast way to do this in elixir:

```elixir
  def bit_count(n) do
    for(<<bit::1 <- :binary.encode_unsigned(n)>>, do: bit) |> Enum.sum()
  end
```

## Solutions

- [Elixir](../elixir2016/lib/day13.ex)

## Problem Description

[2016 Day 13 on AdventOfCode.com](https://adventofcode.com/2016/day/13)

### Part 1

You arrive at the first floor of this new building to discover a much less
welcoming environment than the shiny atrium of the last one. Instead, you are
in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers
(x,y). Each such coordinate is either a wall or an open space. You can't move
diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward
positive x and y; negative values are invalid, as they represent a location
outside the building. You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout
is actually quite logical. You can determine whether a given x,y coordinate
will be a wall or an open space using a simple system:

- Find x*x + 3*x + 2*x*y + y + y\*y.
- Add the office designer's favorite number (your puzzle input).
- Find the binary representation of that sum; count the number of bits that are 1.
  - If the number of bits that are 1 is even, it's an open space.
  - If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing walls
as # and open spaces as ., the corner of the building containing 0,0 would
look like this:

```
  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###
```

Now, suppose you wanted to reach 7,4. The shortest route you could take is
marked as O:

```
  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###
```

Thus, reaching 7,4 would take a minimum of 11 steps (starting from your
current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

### Part 2

How many locations (distinct x,y coordinates, including your starting
location) can you reach in at most 50 steps?
