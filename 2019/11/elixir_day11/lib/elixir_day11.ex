defmodule ElixirDay11 do
  @moduledoc """
  Documentation for ElixirDay11.
  """
  alias ElixirDay11.{Computer, ComputerServer}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def main do
    parse("../../09/input.txt")
    |> Computer.solve([1])
    |> IO.inspect(label: "day 9 part 1")

    parse("../../09/input.txt")
    |> Computer.solve([2])
    |> IO.inspect(label: "day 9 part 2")
  end
end
