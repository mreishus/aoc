defmodule Elixir2020.Day03.GridWithMax do
  alias Elixir2020.Day03.GridWithMax

  defstruct [
    :grid,
    :max_x,
    :max_y
  ]

  def new(grid) when is_map(grid) do
    {max_x, _} = grid |> Map.keys() |> Enum.max_by(fn {x, _y} -> x end)
    {_, max_y} = grid |> Map.keys() |> Enum.max_by(fn {_x, y} -> y end)

    %GridWithMax{
      grid: grid,
      max_x: max_x + 1,
      max_y: max_y + 1
    }
  end
end

defmodule Elixir2020.Day03 do
  alias Elixir2020.Day03.GridWithMax

  def parse() do
    File.stream!("../inputs/03/input.txt")
    |> Enum.map(&String.trim/1)
    |> parse_lines()
  end

  def parse_lines(lines) do
    lines
    |> Enum.zip(0..9999)
    |> Enum.flat_map(&parse_line/1)
    |> Map.new()
    |> GridWithMax.new()
  end

  def parse_line({maze_string, row}) do
    maze_string
    |> String.graphemes()
    |> Enum.zip(0..9999)
    |> Enum.map(fn {char, col} ->
      {{col, row}, char}
    end)
  end

  def grid_at(grid, {x, y}) do
    if y >= grid.max_y do
      :below_field
    else
      x = rem(x, grid.max_x)
      grid.grid |> Map.get({x, y})
    end
  end

  def solve_slope(grid, {dx, dy}) do
    do_solve_slope(grid, {dx, dy}, {0, 0}, 0)
  end

  def do_solve_slope(grid, {dx, dy}, {x, y}, trees_hit) do
    case grid_at(grid, {x, y}) do
      :below_field -> trees_hit
      "#" -> do_solve_slope(grid, {dx, dy}, {x + dx, y + dy}, trees_hit + 1)
      _ -> do_solve_slope(grid, {dx, dy}, {x + dx, y + dy}, trees_hit)
    end
  end

  def part1() do
    slope = {3, 1}

    parse()
    |> solve_slope(slope)
  end

  def part2() do
    grid = parse()

    [
      {1, 1},
      {3, 1},
      {5, 1},
      {7, 1},
      {1, 2}
    ]
    |> Enum.reduce(1, fn slope, acc ->
      acc * solve_slope(grid, slope)
    end)
  end
end
