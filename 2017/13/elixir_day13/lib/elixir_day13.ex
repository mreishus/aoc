defmodule ElixirDay13 do
  alias ElixirDay13.Parse

  @moduledoc """
  Documentation for ElixirDay13.
  """

  @doc """
  Advance scanners 1 step.
  in: layer_map
  out: layer_map
  """
  def advance_scanners(layer_map) do
    Map.keys(layer_map)
    |> Enum.reduce(layer_map, fn i, acc ->
      Map.update(acc, i, nil, fn %{depth: depth, scanner: s, delta: delta} ->
        next_loc = s + delta
        is_bounce = next_loc >= depth or next_loc < 0
        delta = if is_bounce, do: delta * -1, else: delta
        %{depth: depth, scanner: rem(s + delta, depth), delta: delta}
      end)
    end)
  end

  @doc """
   Depth     6
   Position  0 1 2 3 4 5 4 3 2 1 0 1 2 3 4 5 4 3 2 1 0
   Delta     d u u u u u d d d d d u u u u u d d d d d
   Cycle_Pos 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0

   The function takes position + delta and converts it to cycle_pos.

   We're repeating with a cycle length of (depth + depth - 2)
   We need to translate (position, up_or_down) into a one dimensional cycling number
   If U: Simply take the position number
   If D: Example, depth = 6, position 3.  Take 5(max pos) - 3(current pos) = 2, then 2 + 5(maxpos) = 7
  """
  def scanner_cycle_pos(%{depth: _depth, scanner: 0, delta: _delta}), do: 0

  def scanner_cycle_pos(%{depth: _depth, scanner: pos, delta: 1}), do: pos

  def scanner_cycle_pos(%{depth: depth, scanner: pos, delta: -1}) do
    maxpos = depth - 1
    rem(maxpos - pos + maxpos, depth * 2 - 2)
  end

  def scanner_cycle_pos(_), do: raise("Unexpected delta")

  @doc """
  Advance scanners N steps.
  in: layer_map, N
  out: layer_map
  """
  def advance_scanners_n(_layer_map, n) when n < 0,
    do: raise("Can't advance_scanners_n with negative number")

  def advance_scanners_n(layer_map, n) when n == 0, do: layer_map

  def advance_scanners_n(layer_map, n) do
    layer_map
    |> advance_scanners()
    |> advance_scanners_n(n - 1)
  end

  @doc """
  What is the trip severity with no delay?
  """
  def trip_severity(layer_map) do
    trip_severity(layer_map, 0)
  end

  @doc """
  What is the trip severity with a given delay?
  """
  def trip_severity(layer_map, delay) do
    max = Map.keys(layer_map) |> Enum.max()
    layer_map = advance_scanners_n(layer_map, delay)
    do_trip_severity(layer_map, 0, 0, max)
  end

  @doc """
  Calculate one step of trip severity.  Our location advances through the network
  while the scanners move with advance_scanners.  If we're caught, the score
  increases by depth * location.  Note that getting caught at step 0 adds 0
  to the score.
  """
  def do_trip_severity(_layer_map, packet_location, score, max_location)
      when packet_location > max_location do
    score
  end

  def do_trip_severity(layer_map, packet_location, score, max_location) do
    scanner_exists = Map.has_key?(layer_map, packet_location)
    caught = scanner_exists && layer_map[packet_location].scanner == 0
    score = if caught, do: score + packet_location * layer_map[packet_location].depth, else: score
    next_layer_map = advance_scanners(layer_map)

    do_trip_severity(next_layer_map, packet_location + 1, score, max_location)
  end

  @doc """
  Does moving through the map at layer_map get caught?
  This is like the trip severity function, but it stops simulating as soon
  as we're caught.
  """
  def caught?(layer_map) do
    max = Map.keys(layer_map) |> Enum.max()
    do_caught?(layer_map, 0, max)
  end

  def do_caught?(_layer_map, packet_location, max_location) when packet_location > max_location,
    do: false

  def do_caught?(layer_map, packet_location, max_location) do
    scanner_exists = Map.has_key?(layer_map, packet_location)
    caught = scanner_exists && layer_map[packet_location].scanner == 0

    if caught do
      true
    else
      next_layer_map = advance_scanners(layer_map)
      do_caught?(next_layer_map, packet_location + 1, max_location)
    end
  end

  @doc """
  Does moving through the map at layer_map get caught?
  Uses modulo to only calculate the final position of each scanner,
  instead of stepping forward all layers at all steps.
  """
  def fast_caught?(layer_map, delay) do
    layer_map
    |> Stream.map(fn {index, layer} ->
      rem(delay + scanner_cycle_pos(layer) + index, layer.depth * 2 - 2)
    end)
    |> Enum.any?(fn pos -> pos == 0 end)
  end

  @doc """
  What is the lowest delay we can move through the network without being caught?
  Uses a simulation approach.  Takes 2 minutes on my computer..
  """
  def part2_sim(layer_map) do
    do_part2(layer_map, 0)
  end

  def do_part2(layer_map, delay) do
    if not caught?(layer_map) do
      delay
    else
      layer_map = advance_scanners(layer_map)
      do_part2(layer_map, delay + 1)
    end
  end

  def part2_mod(layer_map) do
    part2_mod(layer_map, 0)
  end

  def part2_mod(layer_map, delay) do
    if not fast_caught?(layer_map, delay) do
      delay
    else
      part2_mod(layer_map, delay + 1)
    end
  end

  def main do
    Parse.parse_file("../input.txt")
    |> trip_severity()
    |> IO.inspect(label: "Part 1")

    Parse.parse_file("../input.txt")
    |> part2_mod()
    |> IO.inspect(label: "Part 2")
  end
end
