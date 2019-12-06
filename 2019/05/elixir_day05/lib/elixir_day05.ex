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

    parse("../input.txt")
    |> Computer.solve([5])
    |> IO.inspect(label: "part2")
  end

  def benchmark do
    program = parse("../input.txt")

    Benchee.run(%{
      "part1" => fn -> Computer.solve(program, [1]) end,
      "part2" => fn -> Computer.solve(program, [5]) end
    })
  end
end
