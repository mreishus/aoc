defmodule Square do
  defstruct [
    coord_index: nil,
    assigned_coord: nil,
    is_infinite: false,
  ]
end

defmodule AdventOfCode201806 do
  @moduledoc """
  Documentation for AdventOfCode201806.
  """

  alias AdventOfCode201806.ParseFile, as: ParseFile

  @doc """
  iex> AdventOfCode201806.find_first_index_in_list(["square", "triangle", "rect"], "rect")
  2
  iex> AdventOfCode201806.find_first_index_in_list(["square", "triangle", "rect"], "square")
  0
  iex> AdventOfCode201806.find_first_index_in_list(["square", "triangle", "rect"], "missing")
  nil
  """
  def find_first_index_in_list(list, needle) do
    matches = list
      |> Enum.zip(0..length(list)) 
      |> Enum.filter(fn {x, _} -> x == needle end)
    case matches do
      [] -> nil
      _ -> matches |> List.first |> elem(1)
    end
  end

  @doc """
  iex> AdventOfCode201806.distance(1, 1, 4, 3)
  5
  """
  def distance(x1, y1, x2, y2), do: abs(x1 - x2) + abs(y1 - y2)

  @doc """
  iex> AdventOfCode201806.find_closest( [ {1, 1}, {1, 6}, {8, 3}, {3, 4}, {5, 5}, {8, 9} ], {4, 4} )
  3
  iex> AdventOfCode201806.find_closest( [ {1, 1}, {1, 6}, {8, 3}, {3, 4}, {5, 5}, {8, 9} ], {5, 0} )
  -1
  """
  def find_closest(coords, {x, y}) do
    answers = coords
      |> Stream.with_index
      |> Enum.reduce([], fn ({{coord_x, coord_y}, i}, acc) ->
        dist = distance(coord_x, coord_y, x, y)
        record = %{ coord_i: i, dist: dist }
        [ record | acc ]
      end)
      |> Enum.sort_by(fn x -> x.dist end)

    #IO.inspect answers

    [first | [ second | _rest ]] = answers
    case first.dist == second.dist do
      true -> -1 # Tie
      false -> first.coord_i
    end
  end

  @doc """
  iex> AdventOfCode201806.coords_to_board_size([{1, 1}, {8, 9}])
  {9, 10}
  """
  def coords_to_board_size(coords) do
    max_x = coords |> Enum.map(fn x -> elem(x, 0) end) |> Enum.max
    max_y = coords |> Enum.map(fn x -> elem(x, 1) end) |> Enum.max
    # Adding one space on all dimensions
    # For example, if coords go from 1-5, we have board 0-6
    {max_x + 1, max_y + 1} 
  end

  def generate_board(coords) do
    {size_x, size_y} = coords_to_board_size(coords)

    # loop entire grid
    0..size_x |> Enum.reduce(%{}, fn x, acc ->
      0..size_y |> Enum.reduce(acc, fn y, acc ->

        # compute square
        this_square = %Square{
          coord_index: find_first_index_in_list(coords, {x, y}),
          assigned_coord: find_closest(coords, {x, y}),
          is_infinite: x == 0 || y == 0 || x == size_x || y == size_y,
        }

        # stick square in map
        {_, map} = Map.get_and_update(acc, {x, y}, fn current_value ->
          {current_value, this_square}
        end)
        map

      end)
    end)
  end

  def go do
    true
  end

  @doc """
  iex> AdventOfCode201806.part1()
  true
  """
  def part1(filename \\ "input_small.txt") do
    coords = ParseFile.filename_to_coords(filename)
    grid = generate_board(coords)

    #IO.inspect(grid)
    true
  end
end
