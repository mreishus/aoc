defmodule Elixir2024 do
  alias Elixir2024.{Day01, Day02}

  def day1to5 do
    Day01.part1("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 1")

    Day01.part2("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 2")
  end

  def wip() do
    Day02.part1("../inputs/02/input_small.txt")
    |> IO.inspect(label: "2024 Day 02 Part 1")

    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2024 Day 02 Part 1")

    Day02.part2("../inputs/02/input_small.txt")
    |> IO.inspect(label: "2024 Day 02 Part 2")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2024 Day 02 Part 2")
  end

  def main do
    # day1to5()
    # day6to10()
    # day11to15()
    wip()
  end
end
