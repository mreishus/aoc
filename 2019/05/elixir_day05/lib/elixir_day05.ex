defmodule ElixirDay05 do
  @moduledoc """
  Documentation for ElixirDay05.
  """

  alias ElixirDay05.Computer

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def main do
    parse("../input.txt")
    |> Computer.solve([1])
    |> IO.inspect(label: "part1")
  end
end
