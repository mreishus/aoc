defmodule Elixir2015 do
  alias Elixir2015.Day01
  alias Elixir2015.Day02
  alias Elixir2015.Day03
  alias Elixir2015.Day04

  def day1to5 do
    Day01.part1()
    |> IO.inspect(label: "2015 Day 01 Part 1")

    Day01.part2()
    |> IO.inspect(label: "2015 Day 01 Part 2")

    Day02.part1()
    |> IO.inspect(label: "2015 Day 02 Part 1")

    Day02.part2()
    |> IO.inspect(label: "2015 Day 02 Part 2")

    Day03.part1()
    |> IO.inspect(label: "2015 Day 03 Part 1")

    Day03.part2()
    |> IO.inspect(label: "2015 Day 03 Part 2")

    Day04.part1()
    |> IO.inspect(label: "2015 Day 04 Part 1")

    Day04.part2()
    |> IO.inspect(label: "2015 Day 04 Part 2")
  end

  def main do
    day1to5()
  end
end
