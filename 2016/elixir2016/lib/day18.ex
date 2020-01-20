defmodule Elixir2016.Day18 do
  use Bitwise

  def parse(filename) do
    File.read!(filename)
    |> String.trim()
  end

  def part1(filename) do
    parse(filename)
    |> String.graphemes()
    |> digitify()
    |> part1_count(40)
  end

  def part2(filename) do
    parse(filename)
    |> String.graphemes()
    |> digitify()
    |> part1_count(400_000)
  end

  def part1_count(initial_row, num_rows), do: do_part1_count(initial_row, num_rows, 0)

  def do_part1_count(_initial_row, 0, n), do: n

  def do_part1_count(initial_row, num_rows, n) do
    next_row = next_row(initial_row)

    this_row_count =
      initial_row
      |> Enum.filter(fn x -> x == 0 end)
      |> length()

    do_part1_count(next_row, num_rows - 1, n + this_row_count)
  end

  @doc """
  iex(2)> Day18.digitify([ ".", ".", "^", "^" ])
  [0, 0, 1, 1]
  """
  def digitify(list) do
    list
    |> Enum.map(fn x ->
      case x do
        "^" -> 1
        "." -> 0
        _ -> raise "Invalid input"
      end
    end)
  end

  @doc """
  iex(2)> Day18.next_row([ 0, 0, 1, 1, 0 ])
  [0, 1, 1, 1, 1]
  """
  def next_row(list) do
    list
    |> extended_three_window()
    |> Enum.map(fn [left, _mid, right] ->
      left ^^^ right
    end)
  end

  @doc """
  window: Moves a sliding window over a list

  iex(2)> ["a", "b", "c", "d", "e"] |> Day18.window(2)
  [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"]]

  iex(3)> ["a", "b", "c", "d", "e"] |> Day18.window(3)
  [["a", "b", "c"], ["b", "c", "d"], ["c", "d", "e"]]
  """
  def window([_x | xs] = list, size) do
    if length(list) < size do
      []
    else
      [Enum.take(list, size)] ++ window(xs, size)
    end
  end

  def window(_, _), do: []

  @doc """
  Extended three window:
  Adds "." and "." to the beginning/end of a list, then calls window 3 on that new list.
  Gets you a list of 3 for each item in the original list, 
  with the original item being in the center of the three.

  iex(10)> ["aa", "bb", "cc", "dd", "ee"] |> Day18.extended_three_window()
  [
      [".", "aa", "bb"],
      ["aa", "bb", "cc"],
      ["bb", "cc", "dd"],
      ["cc", "dd", "ee"],
      ["dd", "ee", "."]
  ]
  """
  def extended_three_window(list) do
    ([0 | list] ++ [0])
    |> window(3)
  end
end
