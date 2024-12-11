defmodule Elixir2024.Day04 do
  def parse(filename) do
    grid =
      File.stream!(filename)
      |> Stream.map(&String.trim/1)
      |> Stream.reject(&(&1 == ""))
      |> Enum.zip(0..9999)
      |> Enum.flat_map(fn {line, y} ->
        line
        |> String.graphemes()
        |> Enum.with_index()
        |> Enum.map(fn {char, x} -> {{x, y}, char} end)
      end)
      |> Map.new()

    keys = Map.keys(grid)
    {max_x, _} = Enum.max_by(keys, fn {x, _y} -> x end)
    {_, max_y} = Enum.max_by(keys, fn {_x, y} -> y end)

    %{
      grid: grid,
      max_x: max_x,
      max_y: max_y
    }
  end

  def part1(filename) do
    data = parse(filename)
    find_word(data, "XMAS")
  end

  def part2(filename) do
    parse(filename)
    |> find_x()
  end

  ### Part 1 Helpers

  def get_directions() do
    [
      {1, 0},
      {-1, 0},
      {0, 1},
      {0, -1},
      {1, 1},
      {-1, 1},
      {1, -1},
      {-1, -1}
    ]
  end

  def find_word(%{grid: _grid, max_x: max_x, max_y: max_y} = data, word) do
    word_length = String.length(word)
    starting_positions = for x <- 0..max_x, y <- 0..max_y, do: {x, y}

    # For each (position*direction), check if word starts there
    for(
      pos <- starting_positions,
      dir <- get_directions(),
      check_word_at_position(data, pos, dir, word, word_length),
      do: 1
    )
    |> Enum.sum()
  end

  def check_word_at_position(
        %{grid: grid, max_x: max_x, max_y: max_y},
        {start_x, start_y},
        {dx, dy},
        word,
        length
      ) do
    # Make all the coordinates for this position+direction combo
    positions = for i <- 0..(length - 1), do: {start_x + dx * i, start_y + dy * i}

    # First - are all coordinates in bounds?
    if Enum.all?(positions, fn {x, y} ->
         x >= 0 and x <= max_x and y >= 0 and y <= max_y
       end) do
      # Then check if the word matches
      word ==
        positions
        |> Enum.map(&grid[&1])
        |> Enum.join()
    else
      false
    end
  end

  ### Part 2 Helpers

  def find_x(%{grid: grid, max_x: max_x, max_y: max_y}) do
    for(
      x <- 0..max_x,
      y <- 0..max_y,
      # First, check if center is 'A'
      grid[{x + 1, y + 1}] == "A",
      # Check first diagonal
      {slash_one_a, slash_one_b} = {grid[{x, y}], grid[{x + 2, y + 2}]},
      valid_diagonal?({slash_one_a, slash_one_b}),
      # Check second diagonal
      {slash_two_a, slash_two_b} = {grid[{x + 2, y}], grid[{x, y + 2}]},
      valid_diagonal?({slash_two_a, slash_two_b}),
      do: 1
    )
    |> Enum.sum()
  end

  def valid_diagonal?({a, b}) do
    (a == "M" and b == "S") or (a == "S" and b == "M")
  end
end
