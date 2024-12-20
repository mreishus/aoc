defmodule Elixir2024 do
  alias Elixir2024.{Day01, Day02, Day03, Day04}

  def day1to5 do
    Day01.part1("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 1")

    Day01.part2("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 2")

    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2024 Day 02 Part 1")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2024 Day 02 Part 2")

    Day03.part1("../inputs/03/input.txt")
    |> IO.inspect(label: "2024 Day 03 Part 1")

    Day03.part2("../inputs/03/input.txt")
    |> IO.inspect(label: "2024 Day 03 Part 2")

    Day04.part1("../inputs/04/input.txt")
    |> IO.inspect(label: "2024 Day 04 Part 1")

    Day04.part2("../inputs/04/input.txt")
    |> IO.inspect(label: "2024 Day 04 Part 2")
  end

  def wip() do
    Day04.part1("../inputs/04/input_small.txt")
    |> IO.inspect(label: "2024 Day 04 Part 1")

    Day04.part1("../inputs/04/input.txt")
    |> IO.inspect(label: "2024 Day 04 Part 1")

    Day04.part2("../inputs/04/input_small.txt")
    |> IO.inspect(label: "2024 Day 04 Part 2")

    Day04.part2("../inputs/04/input.txt")
    |> IO.inspect(label: "2024 Day 04 Part 2")
  end

  def main do
    # day1to5()
    # day6to10()
    # day11to15()
    wip()
  end
end
