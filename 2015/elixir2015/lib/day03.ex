defmodule Elixir2015.Day03 do
  def parse() do
    File.read!("../inputs/03/input.txt")
    |> String.graphemes()
    |> Enum.map(&char_to_dir/1)
  end

  def char_to_dir("v"), do: {0, -1}
  def char_to_dir("^"), do: {0, 1}
  def char_to_dir(">"), do: {1, 0}
  def char_to_dir("<"), do: {-1, 0}

  def move({x0, y0}, {x1, y1}), do: {x0 + x1, y0 + y1}

  # Turn a list of steps into a map representing how many
  # coordinates were visited, and how many times they were visited
  # as value.
  def visited(steps) do
    visited = %{{0, 0} => 1}
    loc = {0, 0}

    {visited, _loc} =
      steps
      |> Enum.reduce({visited, loc}, fn step, {visited, loc} ->
        loc = move(loc, step)

        visited =
          visited
          |> Map.update(loc, 1, fn x -> x + 1 end)

        {visited, loc}
      end)

    visited
  end

  # Turn a list of steps into a map representing how many
  # coordinates were visited, and how many times they were visited
  # as value.
  # This time, there are two agents walking who alternate turns.
  def visited_with_robot(steps) do
    visited = %{{0, 0} => 1}
    locs = [{0, 0}, {0, 0}]
    turn = 0

    {visited, _locs, _turn} =
      steps
      |> Enum.reduce({visited, locs, turn}, fn step, {visited, locs, turn} ->
        new_loc = move(locs |> Enum.at(turn), step)

        visited =
          visited
          |> Map.update(new_loc, 1, fn x -> x + 1 end)

        locs = locs |> List.replace_at(turn, new_loc)

        {visited, locs, flip_turn(turn)}
      end)

    visited
  end

  def flip_turn(0), do: 1
  def flip_turn(1), do: 0

  def part1() do
    parse()
    |> visited()
    |> Map.keys()
    |> Enum.count()
  end

  def part2() do
    parse()
    |> visited_with_robot()
    |> Map.keys()
    |> Enum.count()
  end
end
