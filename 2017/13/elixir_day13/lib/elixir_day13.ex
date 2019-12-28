defmodule ElixirDay13 do
  alias ElixirDay13.Parse

  @moduledoc """
  Documentation for ElixirDay13.
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

  def trip_severity(layer_map) do
    max = Map.keys(layer_map) |> Enum.max()
    do_trip_severity(layer_map, 0, 0, max)
  end

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

  def main do
    Parse.parse_file("../input.txt")
    |> trip_severity()
    |> IO.inspect(label: "Part 1")
  end
end
