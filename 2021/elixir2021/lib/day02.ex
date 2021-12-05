defmodule Elixir2021.Day02 do
  @doc """
  parse/1: Given a filename,
  Create a list like [
    ["down", 9],
    ["forward", 3],
    ["up", 8],
    ...
  ]
  """
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.split/1)
    |> Stream.map(fn [command, num] -> [command, String.to_integer(num)] end)
  end

  def part1(filename) do
    parse(filename)
    |> Enum.reduce({0, 0}, fn [command, num], {x, z} ->
      case command do
        "forward" ->
          {x + num, z}

        "down" ->
          {x, z + num}

        "up" ->
          {x, z - num}
      end
    end)
    |> multiply_coords()
  end

  def part2(filename) do
    parse(filename)
    |> Enum.reduce({0, 0, 0}, fn [command, num], {x, z, aim} ->
      case command do
        "forward" ->
          {x + num, z + aim * num, aim}

        "down" ->
          {x, z, aim + num}

        "up" ->
          {x, z, aim - num}
      end
    end)
    |> multiply_coords()
  end

  def multiply_coords({x, z}), do: x * z
  def multiply_coords({x, z, _aim}), do: x * z
end
