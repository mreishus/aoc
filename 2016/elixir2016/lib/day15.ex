defmodule Elixir2016.Day15 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse_line/1)
    |> Stream.with_index()
    |> Stream.map(fn {disc, index} ->
      Map.put(disc, :index, index + 1)
    end)
    |> Enum.to_list()
  end

  def parse_line(line) do
    # Disc #1 has 17 positions; at time=0, it is at position 15.
    parser = ~r/Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+)\./

    [num_pos, init_pos] =
      Regex.run(parser, line)
      |> Enum.drop(1)
      |> Enum.map(&String.to_integer/1)

    %{num_pos: num_pos, init_pos: init_pos}
  end

  def part1(filename) do
    discs = parse(filename)

    Stream.iterate(0, fn x -> x + 1 end)
    |> Stream.filter(fn delay ->
      discs
      |> Enum.all?(fn disc -> drop_position(disc, delay) == 0 end)
    end)
    |> Enum.take(1)
  end

  def part2(filename) do
    discs = parse(filename)
    discs = discs ++ [%{index: 7, init_pos: 0, num_pos: 11}]

    Stream.iterate(0, fn x -> x + 1 end)
    |> Stream.filter(fn delay ->
      discs
      |> Enum.all?(fn disc -> drop_position(disc, delay) == 0 end)
    end)
    |> Enum.take(1)
  end

  def drop_position(disc, delay) when is_map(disc) and is_integer(delay) do
    pos = disc.init_pos + delay + disc.index
    pos = rem(pos, disc.num_pos)
  end
end
