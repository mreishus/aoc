defmodule Elixir2016.Day04 do
  alias Elixir2016.Day04.Rotate

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse_room/1)
  end

  def part1(filename) do
    parse(filename)
    |> Stream.filter(&valid_room?/1)
    |> Enum.map(fn room -> room.sector_id end)
    |> Enum.sum()
  end

  def part2(filename) do
    parse(filename)
    |> Stream.filter(&valid_room?/1)
    |> Stream.map(&add_real_name/1)
    |> Stream.filter(&north_pole?/1)
    |> Stream.map(fn room -> room.sector_id end)
    |> Enum.at(0)
  end

  def add_real_name(room) do
    real_name =
      room.name
      |> Rotate.rotate(room.sector_id)
      |> String.replace("-", " ")

    room |> Map.put(:real_name, real_name)
  end

  def north_pole?(room) do
    room.real_name
    |> String.downcase()
    |> String.contains?("northpole")
  end

  def parse_room(string) do
    [_, name, sector_id, checksum] = Regex.run(~r/^(\D*?)-(\d+)\[(\w+)\]$/, string)
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

defmodule Elixir2016.Day04.Rotate do
  def rotate(string, num) do
    string
    |> String.to_charlist()
    |> Enum.map(fn x -> rotate_codepoint(x, num) end)
    |> List.to_string()
  end

  def rotate_codepoint(x, num) do
    # 97 - 122: a-z
    # 65 - 90: A-Z
    cond do
      97 <= x and x <= 122 ->
        x = x - 97
        x = rem(x + num, 26)
        x + 97

      65 <= x and x <= 90 ->
        x = x - 65
        x = rem(x + num, 26)
        x + 65

      true ->
        x
    end
  end
end
