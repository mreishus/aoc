defmodule Elixir2016.Day04 do
  def part1(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse_room/1)
    |> Stream.filter(&valid_room?/1)
    |> Enum.map(fn room -> room.sector_id end)
    |> Enum.sum()
  end

  def parse_room(string) do
    [_, name, sector_id, checksum] = Regex.run(~r/^(\D*?)(\d+)\[(\w+)\]$/, string)
    %{name: name, sector_id: String.to_integer(sector_id), checksum: checksum}
  end

  def valid_room?(room) when is_map(room) do
    compute_checksum(room) == room.checksum
  end

  def valid_room?(room_str) when is_binary(room_str) do
    room_str
    |> parse_room()
    |> valid_room?
  end

  def compute_checksum(%{name: name} = _room) do
    counts =
      name
      |> String.replace("-", "")
      |> String.graphemes()
      |> Enum.reduce(%{}, fn x, acc ->
        Map.update(acc, x, 1, fn x -> x + 1 end)
      end)

    Map.keys(counts)
    |> Enum.sort_by(fn letter -> {0 - counts[letter], letter} end)
    |> Enum.take(5)
    |> Enum.join("")
  end
end
