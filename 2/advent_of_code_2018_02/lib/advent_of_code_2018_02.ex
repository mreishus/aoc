defmodule AdventOfCode201802 do
  @moduledoc """
  Documentation for AdventOfCode201802.
  """

  @doc """
  Hello world.

  ## Examples

      iex> AdventOfCode201802.hello()
      :world

  """
  def hello do
    :world
  end

  def get_char_counts(str) do
    str 
      |> String.graphemes
      |> Enum.reduce(%{}, fn(x, acc) -> Map.put(acc, x, (acc[x] || 0) + 1) end)
  end

  def char_count_contains_num(char_count, desired_count) do
    char_count
      |> Map.values
      |> Enum.member?(desired_count)
  end

  def read_file() do
    file_name = Path.expand("./", __DIR__) |> Path.join("input.txt")
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  def part1 do
    data = read_file()

    two_count = data 
      |> Enum.filter(fn x -> get_char_counts(x) |> char_count_contains_num(2) end) 
      |> Enum.count
    three_count = data 
      |> Enum.filter(fn x -> get_char_counts(x) |> char_count_contains_num(3) end) 
      |> Enum.count
    IO.puts "[Part1] Checksum is:"
    IO.puts two_count * three_count
  end

  def part2 do
    IO.puts "Part 2"
  end
  def both_parts do
    part1()
    part2()
  end
end
