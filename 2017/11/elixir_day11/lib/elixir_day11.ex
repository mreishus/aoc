defmodule ElixirDay11 do
  @moduledoc """
  Documentation for ElixirDay11.
  """

  # Move in hex grid, using cube coordinates
  # See https://www.redblobgames.com/grids/hexagons/#neighbors-cube
  def move({x, y, z}, "nw"), do: {x - 1, y + 1, z + 0}
  def move({x, y, z}, "n"), do: {x + 0, y + 1, z - 1}
  def move({x, y, z}, "ne"), do: {x + 1, y + 0, z - 1}
  def move({x, y, z}, "sw"), do: {x - 1, y + 0, z + 1}
  def move({x, y, z}, "s"), do: {x + 0, y - 1, z + 1}
  def move({x, y, z}, "se"), do: {x + 1, y - 1, z + 0}

  # Given cube coordinates, how many steps away from the origin?
  def steps_away({x, y, z}) do
    [x, y, z]
    |> Enum.map(&abs/1)
    |> Enum.max()
  end

  def part1(directions) when is_list(directions) do
    directions
    |> Enum.reduce({0, 0, 0}, fn dir, acc ->
      move(acc, dir)
    end)
    |> steps_away()
  end

  def part2(directions) when is_list(directions) do
    initial_acc = %{coord: {0, 0, 0}, max_steps: 0}

    directions
    |> Enum.reduce(initial_acc, fn dir, acc ->
      new_coord = move(acc.coord, dir)
      %{coord: new_coord, max_steps: Enum.max([acc.max_steps, steps_away(new_coord)])}
    end)
    |> Map.get(:max_steps)
  end

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
  end

  def main do
    parse("../input.txt")
    |> part1()
    |> IO.inspect(label: "Part 1")

    parse("../input.txt")
    |> part2()
    |> IO.inspect(label: "Part 2")
  end
end
