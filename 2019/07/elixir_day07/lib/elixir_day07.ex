defmodule ElixirDay07 do
  @moduledoc """
  Documentation for ElixirDay07.
  """
  alias ElixirDay07.Computer

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def main do
    parse("../../05/input.txt")
    |> Computer.solve([1])
    |> IO.inspect(label: "day 5 part1")

    parse("../../05/input.txt")
    |> Computer.solve([5])
    |> IO.inspect(label: "day 5 part2")
  end
end
