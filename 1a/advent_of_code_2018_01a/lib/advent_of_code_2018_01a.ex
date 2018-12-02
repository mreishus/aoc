defmodule AdventOfCode201801a do
  @moduledoc """
    Author: Matthew Reishus
    Date: 2018-12-01
    Purpose: Advent Of Code 2018, Day 1, Puzzle 1

    Program reads a text file in "input.txt" comprised of lines like
    "+5", "-100" or "+89". All lines begin with either "-" or "+".

    It returns the sum of all of the numbers.  For example, a file containing
    "+1", "+2", "+100", "-50" will return "53".
  """

  @doc """
    compute_input_sum: Reads all lines in input.txt, sums them, and prints the
    sum to console.
  """
  def read_file() do
    file_name = Path.expand("./", __DIR__) |> Path.join("input.txt")
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
      |> Enum.map(fn x -> String.to_integer(x) end)
  end

  # Sum, calls Enum.sum, Pretty much pointless but allows for logic change and unit test
  def sum(list), do: list |> Enum.sum

  def compute_input_sum(), do: read_file() |> sum |> IO.puts
end

