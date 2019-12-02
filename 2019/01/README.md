# Day 1: The Tyranny of the Rocket Equation

## Approach and Reflections

This was a fairly simple problem based around parsing a file full of numbers
and applying some basic math. This is a good way to ease into Advent of Code
and to try out a new language.

## Solutions

- [Ruby](./ruby_day01/01.rb)
- [Elixir](./elixir_day01/lib/elixir_day01.ex) - Uses tail call optimization
- [Go](./go_day01/day01.go)
- [Python](./python_day01/day01.py)
- [Raku](./raku_day01/01.p6)
- [Crystal](./crystal_day01/src/crystal_day01.cr)

## Solutions (Fan-made Large Input)

`input_large.txt` is a fan made input containing 1,000,000 lines of numbers 46
digits long.

- [Elixir](./elixir_day01/lib/elixir_day01_big.ex) - After implementing Flow,
  solves in 4.7 seconds on my quad core laptop. `make big` to run. Was 19
  seconds without concurrency.
- [Go](./go_day01/day01_large.go) - Runs in 7 seconds using BigNum and
  channels. Adding channels to Part 1 actually slowed it down, but I might
  not be implementing them here in the best way.

Overall, Elixir made solving the large input very easy. It supports BigNums
out of the box - all ints have large support by default - I was using them all
along, which I didn't expect. The `Flow` library provided one way to
parallelize the work easily, but I also tried a manual implementation which
was just as fast.

- [Elixir Manual](./elixir_day01/lib/elixir_day01_big.ex) - Manual
  chunking/parallelize: 5 seconds.
- [Elixir Flow](./elixir_day01/lib/elixir_day01_big_flow.ex) - Using Flow
  library: 5 seconds.
- [Elixir Naive](./elixir_day01/lib/elixir_day01_big_naive.ex) - Spawning one
  million processes at once. Slow: 35 seconds. It's actually faster to run in
  one process, but hey, I wanted to spawn a million.

On the other hand, my Go program needed to be converted to use big.Int, which
was not fun. All of the basic operations need their own function calls, and
they expect you to pass pointers to BigInts around, not the actual values.
When it came to adding concurrency, I first tried passing pointers across the
channels but the program paniced and crashed. So I changed to values.. it
ended up working, but it was a bit of a `*` and `&` soup, which I didn't like.

## Visualization

I made some visualizations of the problem using react-three-fiber. They're
quite crude, with relative box area representing the amount of fuel used for
each number, but it's my first time using react-three-fiber to draw in 3d, so
I'm satisfied.

![Day 1 Part 1 Visualization](./2019_day01_part1.gif?raw=true "Day 1 Part 1 Visualization")

![Day 1 Part 2 Visualization](./2019_day01_part2.gif?raw=true "Day 1 Part 2 Visualization")

## Problem Description

[2019 Day 01 on AdventOfCode.com](https://adventofcode.com/2019/day/1)

### Part One

The Elves quickly load you into a spacecraft and prepare to launch.

At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper.
They haven't determined the amount of fuel required yet.

Fuel required to launch a given **module** is based on its **mass**.
Specifically, to find the fuel required for a module, take its mass, divide by
three, round down, and subtract 2.

For example:

- For a mass of `12`, divide by 3 and round down to get `4`, then subtract
  2 to get `2`.
- For a mass of `14`, dividing by 3 and rounding down still yields `4`, so the
  fuel required is also `2`.
- For a mass of `1969`, the fuel required is `654`.
- For a mass of `100756`, the fuel required is `33583`.

The Fuel Counter-Upper needs to know the total fuel requirement. To find it,
individually calculate the fuel needed for the mass of each module (your
puzzle input), then add together all the fuel values.

**What is the sum of the fuel requirements** for all of the modules on your spacecraft?

### Part Two

During the second Go / No Go poll, the Elf in charge of the Rocket Equation
Double-Checker stops the launch sequence. Apparently, you forgot to include
additional fuel for the fuel you just added.

Fuel itself requires fuel just like a module - take its mass, divide by three,
round down, and subtract 2. However, that fuel **also** requires fuel, and
**that** fuel requires fuel, and so on. Any mass that would require **negative
fuel** should instead be treated as if it requires **zero fuel**; the
remaining mass, if any, is instead handled by **wishing really hard**, which
has no mass and is outside the scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total. Then,
treat the fuel amount you just calculated as the input mass and repeat the
process, continuing until a fuel requirement is zero or negative. For example:

- A module of mass `14` requires `2` fuel. This fuel requires no further fuel
  (2 divided by 3 and rounded down is `0`, which would call for a negative
  fuel), so the total fuel required is still just `2`.
- At first, a module of mass `1969` requires `654` fuel. Then, this fuel
  requires `216` more fuel (`654 / 3 - 2`). `216` then requires `70` more
  fuel, which requires `21` fuel, which requires `5` fuel, which requires no
  further fuel. So, the total fuel required for a module of mass `1969` is
  `654 + 216 + 70 + 21 + 5 = 966`.
- The fuel required by a module of mass `100756` and its fuel is: `33583
  - 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346`.

**What is the sum of the fuel requirements** for all of the modules on your
spacecraft when also taking into account the mass of the added fuel?
(Calculate the fuel requirements for each module separately, then add them all
up at the end.)
