# ExecutionTime.time_of(fn -> Day01.part1() end, [])
defmodule ExecutionTime do
  def time_of(function, args) do
    {uSecs, _val} = :timer.tc(function, args)
    IO.puts("Time: #{uSecs / 1_000}ms")
  end
end

defmodule Elixir2021 do
  alias Elixir2021.{Day01, Day02}

  def day1to5 do
    Day01.part1("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 1")

    Day01.part2("../inputs/01/input.txt")
    |> IO.inspect(label: "2021 Day 01 Part 2")

    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2021 Day 02 Part 1")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2021 Day 02 Part 2")
  end

  def main do
    day1to5()
  end
end
