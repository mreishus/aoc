defmodule ElixirDay03 do
  @moduledoc """
  Documentation for ElixirDay03.
  """

  @doc """
   Turns a filename into a list of "wires".  A wire is a map.
   See parse_line below for more info about wires.
  """
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(&parse_line/1)
  end

  @doc """
   Turns a string into a "wire".  A wire is a map with keys like {x, y}
   representing grid coordinates.  The value is the number of steps taken to
   reach that coordinate.
  """
  def parse_line(string) do
    # When building a wire, we use a tuple of {visited, location, steps}.
    # Visited is the map described above.
    # Location is {x, y}, our current location.
    # Steps is an int, current number of steps taken.
    {visited, _location, _steps} =
      string
      |> String.trim()
      |> String.split(",")
      |> Enum.map(&parse_step/1)
      |> Enum.reduce({%{}, {0, 0}, 0}, fn %{direction: direction, distance: distance}, acc ->
        1..distance
        |> Enum.reduce(acc, fn _, {visited, location, steps} ->
          new_steps = steps + 1
          new_location = move(location, direction)

          # Possible bug: Self intersection overwrites "steps taken" with the later amount of steps
          new_visited = Map.put(visited, new_location, new_steps)
          {new_visited, new_location, new_steps}
        end)
      end)

    visited
  end

  # parse_step("U58") -> %{direction: "U", distance: 58}
  def parse_step(step) do
    direction = String.slice(step, 0, 1)
    distance = String.slice(step, 1, String.length(step) - 1) |> String.to_integer()
    %{direction: direction, distance: distance}
  end

  def move({x, y}, "R"), do: {x + 1, y}
  def move({x, y}, "L"), do: {x - 1, y}
  def move({x, y}, "U"), do: {x, y + 1}
  def move({x, y}, "D"), do: {x, y - 1}
  def move({_x, _y}, _), do: raise("move: unknown direction")

  @doc """
  Find all intersecting wires, convert the intersecting points to manhattan distance,
  find the smallest manhattan distance.
  """
  def part1(wires) do
    wires
    |> Enum.map(&Map.keys/1)
    |> Enum.map(&MapSet.new/1)
    |> Enum.reduce(&MapSet.intersection/2)
    |> Enum.map(fn {x, y} -> abs(x) + abs(y) end)
    |> Enum.min()
  end

  @doc """
  Find all intersecting wires, convert the intersecting points to cumulative steps
  taken by all wires, find the smallest cumulative steps.
  """
  def part2(wires) do
    wires
    |> Enum.map(&Map.keys/1)
    |> Enum.map(&MapSet.new/1)
    |> Enum.reduce(&MapSet.intersection/2)
    |> Enum.map(fn {x, y} -> find_sum_steps(wires, {x, y}) end)
    |> Enum.min()
  end

  @doc """
  Given a list of wires and a coordinate, find the sum of steps taken
  to reach that coordinate.
  """
  def find_sum_steps(wires, {x, y}) do
    wires
    |> Enum.reduce(0, fn wire, acc ->
      acc + wire[{x, y}]
    end)
  end

  def main() do
    wires = parse("../input.txt")

    wires
    |> part1
    |> IO.inspect(label: "Part 1")

    wires
    |> part2
    |> IO.inspect(label: "Part 2")
  end
end
