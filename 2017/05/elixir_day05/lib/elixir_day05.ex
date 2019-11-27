defmodule ElixirDay05 do
  use Tensor

  @moduledoc """
  Documentation for ElixirDay05.
  """

  @doc """
  Hello world.

  ## Examples

      iex> ElixirDay05.hello()
      :world

  """
  def hello do
    :world
  end

  def main do
    IO.puts("Small part1, expect 5: ")

    parse("../input_small.txt")
    |> part1
    |> IO.puts()

    IO.puts("Small part2, expect 10: ")

    parse("../input_small.txt")
    |> part2
    |> IO.puts()

    IO.puts("Large part1: ")

    parse("../input.txt")
    |> part1
    |> IO.puts()

    IO.puts("Large part2: ")

    parse("../input.txt")
    |> part2
    |> IO.puts()
  end

  def part1(jumps) do
    do_part1(jumps, 0, 0)
  end

  def do_part1(jumps, location, steps) do
    value = Vector.get(jumps, location, nil)

    if value == nil do
      steps
    else
      jumps = set(jumps, location, value + 1)
      do_part1(jumps, location + value, steps + 1)
    end
  end

  def part2(jumps) do
    do_part2(jumps, 0, 0)
  end

  def do_part2(jumps, location, steps) do
    value = Vector.get(jumps, location, nil)

    if value == nil do
      steps
    else
      new_val =
        if value >= 3 do
          value - 1
        else
          value + 1
        end

      jumps = set(jumps, location, new_val)
      do_part2(jumps, location + value, steps + 1)
    end
  end

  def set(vector, index, new_value) do
    {:ok, v} = Vector.get_and_update(vector, index, fn _ -> {:ok, new_value} end)
    v
  end

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.to_integer/1)
    |> Enum.map(fn x -> x end)
    |> Vector.new()
  end
end
