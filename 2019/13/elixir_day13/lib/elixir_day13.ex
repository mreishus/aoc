defmodule ElixirDay13 do
  @moduledoc """
  Documentation for ElixirDay13.
  """
  alias ElixirDay13.{Breakout}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def main do
    parse("../../13/input.txt")
    |> Breakout.part1()
    |> IO.inspect(label: "Day 13, Part 1: ")

    parse("../../13/input.txt")
    |> Breakout.part2()
    |> IO.inspect(label: "Day 13, Part 2: ")
  end
end
