defmodule AdventOfCode201806.ParseFile do
  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.trim()
      |> String.split("\n", trim: true)
  end

  @doc """
  parse_coords :: String -> {int, int}
  iex> AdventOfCode201806.ParseFile.parse_coords("3, 4")
  {3, 4}
  """
  def parse_coords(line) do
    [x, y] = line |> String.split(", ", limit: 2) |> Enum.map(&String.to_integer/1)
    {x, y}
  end

  @doc """
  filename_to_coords :: String -> [ {int, int}, ... ]
  iex> AdventOfCode201806.ParseFile.filename_to_coords("input_small.txt")
  [{1, 1}, {1, 6}, {8, 3}, {3, 4}, {5, 5}, {8, 9}]
  """
  def filename_to_coords(filename) do
    filename
      |> read_file()
      |> Enum.map(&parse_coords/1)
  end
end
