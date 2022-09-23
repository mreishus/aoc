# ExecutionTime.time_of(fn -> Day01.part1() end, [])
defmodule ExecutionTime do
  def time_of(function, args) do
    {uSecs, _val} = :timer.tc(function, args)
    IO.puts("Time: #{uSecs / 1_000}ms")
  end
end

defmodule Elixir2021 do
  alias Elixir2021.{Day01, Day02, Day03, Day04, Day05, Day12}

  def day1to5 do
    Day01.part1("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 1")

    Day01.part2("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 2")

    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2021 Day 02 Part 1")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2021 Day 02 Part 2")

    Day03.part1("../inputs/03/input.txt")
    |> IO.inspect(label: "2021 Day 03 Part 1")

    Day03.part2("../inputs/03/input.txt")
    |> IO.inspect(label: "2021 Day 03 Part 2")

    Day04.part1("../inputs/04/input.txt")
    |> IO.inspect(label: "2021 Day 04 Part 1")

    Day04.part2("../inputs/04/input.txt")
    |> IO.inspect(label: "2021 Day 04 Part 2")

    Day05.part1("../inputs/05/input.txt")
    |> IO.inspect(label: "2021 Day 05 Part 1")

    Day05.part2("../inputs/05/input.txt")
    |> IO.inspect(label: "2021 Day 05 Part 2")
  end

  def wip() do
  end

  def day11to15() do
    Day12.part1("../inputs/12/input.txt")
    |> IO.inspect(label: "2021 Day 12 Part 1")

    Day12.part2("../inputs/12/input.txt")
    |> IO.inspect(label: "2021 Day 12 Part 2")
  end

  def main do
    day1to5()
    # day11to15()
    wip()
  end
end
