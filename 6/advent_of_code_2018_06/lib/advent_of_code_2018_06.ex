defmodule AdventOfCode201806 do
  @moduledoc """
  Documentation for AdventOfCode201806.
  """
  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.trim()
      |> String.split("\n", trim: true)
  end

  @doc """
  parse_coords :: String -> {int, int}
  iex> AdventOfCode201806.parse_coords("3, 4")
  {3, 4}
  """
  def parse_coords(line) do
    [x, y] = line |> String.split(", ", limit: 2) |> Enum.map(&String.to_integer/1)
    {x, y}
  end

  @doc """
  filename_to_coords :: String -> [ {int, int}, ... ]
  iex> AdventOfCode201806.filename_to_coords("input_small.txt")
  [{1, 1}, {1, 6}, {8, 3}, {3, 4}, {5, 5}, {8, 9}]
  """
  def filename_to_coords(filename) do
    filename
      |> read_file()
      |> Enum.map(&parse_coords/1)
  end

  def go do
    true
  end

  @doc """
  iex> AdventOfCode201806.part1()
  true
  """
  def part1(filename \\ "input_small.txt") do
    coords = filename_to_coords(filename)
    IO.inspect(coords)
    true
  end
end
