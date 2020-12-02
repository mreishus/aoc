defmodule Elixir2020 do
  alias Elixir2020.Day01

  def day1to5 do
    Day01.part1()
    |> IO.inspect(label: "2020 Day 01 Part 1")

    Day01.part2()
    |> IO.inspect(label: "2020 Day 01 Part 2")
  end

  def main do
    day1to5()
  end
end
