defmodule Elixir2016 do
  alias Elixir2016.{Day02, Day03, Day04, Day05}
  alias Elixir2016.{Day06, Day07, Day09, Day10}
  alias Elixir2016.{Day11, Day12, Day13, Day14, Day15}
  alias Elixir2016.{Day16, Day17, Day18, Day19, Day20}
  alias Elixir2016.{Day21, Day22, Day23, Day24, Day25}

  @moduledoc """
  Documentation for Elixir2016.
  """
  def main do
    day1to5()
    day6to10()
    day11to15()
    day16to20()
    day21to25()
  end

  def latest() do
  end

  def day21to25 do
    Day21.part1("../inputs/21/input.txt")
    |> IO.inspect(label: "2016 Day 21 Part 1")

    Day21.part2("../inputs/21/input.txt")
    |> IO.inspect(label: "2016 Day 21 Part 2")

    Day22.part1("../inputs/22/input.txt")
    |> IO.inspect(label: "2016 Day 22 Part 1")

    Day22.part2("../inputs/22/input.txt")
    |> IO.inspect(label: "2016 Day 22 Part 2")

    Day23.part1("../inputs/23/input.txt")
    |> IO.inspect(label: "2016 Day 23 Part 1")

    Day23.part2("../inputs/23/input.txt")
    |> IO.inspect(label: "2016 Day 23 Part 2")

    Day24.part1("../inputs/24/input.txt")
    |> IO.inspect(label: "2016 Day 24 Part 1")

    Day24.part2("../inputs/24/input.txt")
    |> IO.inspect(label: "2016 Day 24 Part 2")

    Day25.part1("../inputs/25/input.txt")
    |> IO.inspect(label: "2016 Day 25 Part 1")
  end

  def day16to20 do
    Day15.part1("../inputs/15/input.txt")
    |> IO.inspect(label: "2016 Day 15 Part 1")

    Day15.part2("../inputs/15/input.txt")
    |> IO.inspect(label: "2016 Day 15 Part 1")

    Day16.part1("../inputs/16/input.txt")
    |> IO.inspect(label: "2016 Day 16 Part 1")

    "=== Day 16 P2 High Memory (8-10 gigs)" |> IO.inspect()
    # Day 16 part 2: Uses 8+ gigs of memory
    # Day16.part2("../inputs/16/input.txt")
    # |> IO.inspect(label: "2016 Day 16 Part 2")

    Day17.part1("../inputs/17/input.txt")
    |> IO.inspect(label: "2016 Day 17 Part 1")

    Day17.part2("../inputs/17/input.txt")
    |> IO.inspect(label: "2016 Day 17 Part 2")

    Day18.part1("../inputs/18/input.txt")
    |> IO.inspect(label: "2016 Day 18 Part 1")

    Day18.part2("../inputs/18/input.txt")
    |> IO.inspect(label: "2016 Day 18 Part 2")

    Day19.part1("../inputs/19/input.txt")
    |> IO.inspect(label: "2016 Day 19 Part 1")

    Day19.part2("../inputs/19/input.txt")
    |> IO.inspect(label: "2016 Day 19 Part 2")

    Day20.part1("../inputs/20/input.txt")
    |> IO.inspect(label: "2016 Day 20 Part 1")

    Day20.part2("../inputs/20/input.txt")
    |> IO.inspect(label: "2016 Day 20 Part 2")
  end

  def day11to15 do
    Day11.part1()
    |> IO.inspect(label: "2016 Day 11 Part 1")

    "=== Day 11 P2 Slow (3 minutes)" |> IO.inspect()
    # Day11 Part 2 - ~3 minutes
    # Day11.part2()
    # |> IO.inspect(label: "2016 Day 11 Part 2")

    Day12.part1("../inputs/12/input.txt")
    |> IO.inspect(label: "2016 Day 12 Part 1")

    Day12.part2("../inputs/12/input.txt")
    |> IO.inspect(label: "2016 Day 12 Part 2")

    Day13.part1("../inputs/13/input.txt")
    |> IO.inspect(label: "2016 Day 13 Part 1")

    Day13.part2("../inputs/13/input.txt")
    |> IO.inspect(label: "2016 Day 13 Part 2")

    Day14.part1("../inputs/14/input.txt")
    |> IO.inspect(label: "2016 Day 14 Part 1")

    "=== Day 14 P2 Slow (1 Minute)" |> IO.inspect()
    # Day 14 Part2 - Slow, about 1 minute
    # Day14.part2("../inputs/14/input.txt")
    # |> IO.inspect(label: "2016 Day 14 Part 2")
  end

  def day6to10 do
    Day06.part1("../inputs/06/input.txt")
    |> IO.inspect(label: "2016 Day 06 Part 1")

    Day06.part2("../inputs/06/input.txt")
    |> IO.inspect(label: "2016 Day 06 Part 2")

    Day07.part1("../inputs/07/input.txt")
    |> IO.inspect(label: "2016 Day 07 Part 1")

    Day07.part2("../inputs/07/input.txt")
    |> IO.inspect(label: "2016 Day 07 Part 2")

    "=== Day 8 P1 Not implemented in Elixir" |> IO.inspect()
    "=== Day 8 P2 Not implemented in Elixir" |> IO.inspect()

    Day09.part1("../inputs/09/input.txt")
    |> IO.inspect(label: "2016 Day 09 Part 1")

    Day09.part2("../inputs/09/input.txt")
    |> IO.inspect(label: "2016 Day 09 Part 2")

    Day10.part1_and_2("../inputs/10/input.txt")
    |> IO.inspect(label: "2016 Day 10")
  end

  def day1to5 do
    "=== Day 1 P1 Not implemented in elixir" |> IO.inspect()
    "=== Day 1 P2 Not implemented in elixir" |> IO.inspect()

    ## Day 2
    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2016 Day 02 Part 1")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2016 Day 02 Part 2")

    ## Day 3
    Day03.part1("../inputs/03/input.txt")
    |> IO.inspect(label: "2016 Day 03 Part 1")

    Day03.part2("../inputs/03/input.txt")
    |> IO.inspect(label: "2016 Day 03 Part 2")

    ## Day 4
    Day04.part1("../inputs/04/input.txt")
    |> IO.inspect(label: "2016 Day 04 Part 1")

    Day04.part2("../inputs/04/input.txt")
    |> IO.inspect(label: "2016 Day 04 Part 2")

    "=== Day 5 P1 Slow" |> IO.inspect()
    "=== Day 5 P2 Slow" |> IO.inspect()
    ## Day 5 - Slowish - ~1 minute
    # Day05.part1("uqwqemis")
    # |> IO.inspect(label: "2016 Day 05 Part 1")

    # Day05.part2("uqwqemis")
    # |> IO.inspect(label: "2016 Day 05 Part 2")
  end
end
