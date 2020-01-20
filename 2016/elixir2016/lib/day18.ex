defmodule Elixir2016.Day18 do
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
  end

  def part1(filename) do
    parse(filename)
    |> String.graphemes()
    |> part1_count(40)
  end

  def part2(_filename) do
    "p2"
  end

  def part1_count(initial_row, num_rows) do
    all_rows =
      1..(num_rows - 1)
      |> Enum.reduce([initial_row], fn _, acc ->
        new_row = List.last(acc) |> next_row()
        acc ++ [new_row]
      end)

    Enum.concat(all_rows)
    |> Enum.filter(fn x -> x == "." end)
    |> length()
  end

  @doc """
  iex(2)> Day18.next_row([ ".", ".", "^", "^", "." ])
  [".", "^", "^", "^", "^"]
  """
  def next_row(list) do
    list
    |> extended_three_window()
    |> Enum.map(fn [left, mid, right] ->
      t1 = left == "^" and mid == "^" and right == "."
      t2 = left == "." and mid == "^" and right == "^"
      t3 = left == "^" and mid == "." and right == "."
      t4 = left == "." and mid == "." and right == "^"
      t = t1 or t2 or t3 or t4
      if t, do: "^", else: "."
    end)
  end

  @doc """
  window: Moves a sliding window over a list

  iex(2)> ["a", "b", "c", "d", "e"] |> Day18.window(2)
  [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"]]

  iex(3)> ["a", "b", "c", "d", "e"] |> Day18.window(3)
  [["a", "b", "c"], ["b", "c", "d"], ["c", "d", "e"]]
  """
  def window([x | xs] = list, size) do
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
    (["." | list] ++ ["."])
    |> window(3)
  end
end
