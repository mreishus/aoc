# ExecutionTime.time_of(fn -> Day01.part1() end, [])
defmodule ExecutionTime do
  def time_of(function, args) do
    {uSecs, _val} = :timer.tc(function, args)
    IO.puts("Time: #{uSecs / 1_000}ms")
  end
end

defmodule Elixir2021 do
  alias Elixir2021.{Day01, Day02, Day03, Day04, Day05}
  alias Elixir2021.{Day06, Day07, Day12}

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

  def day6to10 do
    Day06.part1("../inputs/06/input.txt")
    |> IO.inspect(label: "2021 Day 06 Part 1")

    Day06.part2("../inputs/06/input.txt")
    |> IO.inspect(label: "2021 Day 06 Part 2")
  end

  def wip() do
    Day07.part1("../inputs/07/input.txt")
    |> IO.inspect(label: "2021 Day 07 Part 1")

    Day07.part2("../inputs/07/input.txt")
    |> IO.inspect(label: "2021 Day 07 Part 2")
  end

  def day11to15() do
    Day12.part1("../inputs/12/input.txt")
    |> IO.inspect(label: "2021 Day 12 Part 1")

    Day12.part2("../inputs/12/input.txt")
    |> IO.inspect(label: "2021 Day 12 Part 2")
  end

  def warning() do
    "" |> IO.puts()
    "---" |> IO.puts()
    "Day 6 uses a Matrix library, which requires BLAS." |> IO.puts()
    "See https://github.com/versilov/matrex" |> IO.puts()
    "I couldn't get this to work, so you can use a slower workaround." |> IO.puts()
    "mix deps.clean --all ; mix deps.get ; MATREX_BLAS=noblas mix compile" |> IO.puts()
    "---" |> IO.puts()
    "" |> IO.puts()
  end

  def main do
    # warning()
    # day1to5()
    # day6to10()
    # day11to15()
    wip()
  end
end
