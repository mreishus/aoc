defmodule Elixir2021.Day05 do
  def parse(filename) do
    File.stream!(filename)
    |> Enum.map(&String.trim/1)
    |> Enum.map(&parse_rules/1)
  end

  def parse_rules(string) do
    # 798,494 -> 135,494
    [_, x1, y1, x2, y2] = Regex.run(~r/^(\d+),(\d+) -> (\d+),(\d+)$/, string)

    %{
      x1: String.to_integer(x1),
      y1: String.to_integer(y1),
      x2: String.to_integer(x2),
      y2: String.to_integer(y2)
    }
  end

  def line_to_coords_diag(line), do: line_to_coords(line, true)
  def line_to_coords(line), do: line_to_coords(line, false)

  def line_to_coords(%{x1: x1, y1: y1, x2: x2, y2: y2}, allow_diag) do
    cond do
      x1 == x2 ->
        y1..y2 |> Enum.map(fn y -> {x1, y} end)

      y1 == y2 ->
        x1..x2 |> Enum.map(fn x -> {x, y1} end)

      allow_diag ->
        x1..x2 |> Enum.zip(y1..y2)

      true ->
        []
    end
  end

  def part1(filename) do
    coords =
      parse(filename)
      |> Enum.flat_map(&line_to_coords/1)

    (coords -- Enum.uniq(coords))
    |> Enum.uniq()
    |> length
  end

  def part2(filename) do
    coords =
      parse(filename)
      |> Enum.flat_map(&line_to_coords_diag/1)

    (coords -- Enum.uniq(coords))
    |> Enum.uniq()
    |> length
  end
end
