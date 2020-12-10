defmodule ExecutionTime do
  def time_of(function, args) do
    {uSecs, _val} = :timer.tc(function, args)
    IO.puts("Time: #{uSecs / 1_000}ms")
  end
end

defmodule Elixir2020 do
  alias Elixir2020.{Day01, Day02, Day03, Day04, Day05}
  alias Elixir2020.{Day06, Day08}

  def day1to5 do
    Day01.part1()
    |> IO.inspect(label: "2020 Day 01 Part 1")

    Day01.part2()
    |> IO.inspect(label: "2020 Day 01 Part 2")

    Day02.part1()
    |> IO.inspect(label: "2020 Day 02 Part 1")

    Day02.part2()
    |> IO.inspect(label: "2020 Day 02 Part 2")

    Day03.part1()
    |> IO.inspect(label: "2020 Day 03 Part 1")

    Day03.part2()
    |> IO.inspect(label: "2020 Day 03 Part 2")

    Day04.part1()
    |> IO.inspect(label: "2020 Day 04 Part 1")

    Day04.part2()
    |> IO.inspect(label: "2020 Day 04 Part 2")

    Day05.part1()
    |> IO.inspect(label: "2020 Day 05 Part 1")

    Day05.part2()
    |> IO.inspect(label: "2020 Day 05 Part 2")
  end

  def day6to10 do
    Day06.part1()
    |> IO.inspect(label: "2020 Day 06 Part 1")

    Day06.part2()
    |> IO.inspect(label: "2020 Day 06 Part 2")

    Day08.part1()
    |> IO.inspect(label: "2020 Day 08 Part 1")

    ExecutionTime.time_of(fn -> Day08.part1() end, [])

    Day08.part2()
    |> IO.inspect(label: "2020 Day 08 Part 2")

    ExecutionTime.time_of(fn -> Day08.part2() end, [])
  end

  def main do
    day1to5()
    day6to10()
  end
end
