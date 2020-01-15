defmodule Elixir2016 do
  alias Elixir2016.{Day02, Day03, Day04, Day05}
  alias Elixir2016.{Day06, Day07, Day09, Day10}

  @moduledoc """
  Documentation for Elixir2016.
  """
  def main do
    day1to5()
    day6to10()
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

    "Day 8 Not implemented in elixir" |> IO.inspect()

    Day09.part1("../inputs/09/input.txt")
    |> IO.inspect(label: "2016 Day 09 Part 1")

    Day09.part2("../inputs/09/input.txt")
    |> IO.inspect(label: "2016 Day 09 Part 2")

    Day10.part1_and_2("../inputs/10/input.txt")
    |> IO.inspect(label: "2016 Day 10")
  end

  def day1to5 do
    "Day 1 Not implemented in elixir" |> IO.inspect()

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

    ## Day 5
    Day05.part1("uqwqemis")
    |> IO.inspect(label: "2016 Day 05 Part 1")

    Day05.part2("uqwqemis")
    |> IO.inspect(label: "2016 Day 05 Part 2")
  end
end
