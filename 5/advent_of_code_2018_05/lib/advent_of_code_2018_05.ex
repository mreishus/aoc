defmodule AdventOfCode201805 do
  @moduledoc """
  Documentation for AdventOfCode201805.
  """
  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.trim()
      |> String.split("\n", trim: true)
  end

  @doc """
  file_to_polymer :: String -> List<Char>
  iex> AdventOfCode201805.file_to_polymer("input_small.txt")
  ["d", "a", "b", "A", "c", "C", "a", "C", "B", "A", "c", "C", "c", "a", "D", "A"]
  """
  def file_to_polymer(filename) do
    read_file(filename)
      |> List.first()
      |> String.graphemes()
  end

  @doc """
  react :: List<Char> -> List<Char>
  Runs the main reaction.
  iex> AdventOfCode201805.react(String.graphemes("dabAaC"))
  String.graphemes("dabC")
  iex> AdventOfCode201805.react(String.graphemes("dabAcCaCBAcCcaDA"))
  String.graphemes("dabCBAcaDA")
  """
  def react(polymer) do
    polymer
    |> Enum.reduce([], fn new_letter, acc ->
      case are_letters_reactive(List.first(acc), new_letter) do
        false -> [new_letter | acc]
        true -> tl(acc)
      end
    end)
    |> Enum.reverse
  end

  @doc """
  are_letters_reactive :: Char -> Char -> Boolean
  Compares two letters to see if there is a reaction between them.

  ## Examples (True)
  iex> AdventOfCode201805.are_letters_reactive("a", "A")
  true
  iex> AdventOfCode201805.are_letters_reactive("A", "a")
  true

  ## Examples (False)
  iex> AdventOfCode201805.are_letters_reactive("a", "a")
  false
  iex> AdventOfCode201805.are_letters_reactive("A", "A")
  false
  iex> AdventOfCode201805.are_letters_reactive("b", "a")
  false
  iex> AdventOfCode201805.are_letters_reactive("b", "A")
  false
  iex> AdventOfCode201805.are_letters_reactive(nil, "A")
  false
  iex> AdventOfCode201805.are_letters_reactive("A", nil)
  false
  """
  def are_letters_reactive(nil, _), do: false
  def are_letters_reactive(_, nil), do: false
  def are_letters_reactive(a, b) do
    a != b && String.downcase(a) == String.downcase(b)
  end

  def part1(filename \\ "input_small.txt") do
    polymer = file_to_polymer(filename)
    react(polymer) |> length
  end

  def all_letters(), do: Enum.to_list(?a .. ?z) |> List.to_string |> String.graphemes

  def part2(filename \\ "input_small.txt") do
    polymer = file_to_polymer(filename)
    all_candidate_lengths = all_letters()
      |> Enum.reduce([], fn letter, acc ->
        this_len = polymer
          |> Enum.join()
          |> String.replace(letter, "")
          |> String.replace(String.upcase(letter), "")
          |> String.graphemes()
          |> react()
          |> length
        [this_len | acc]
      end)
    all_candidate_lengths |> Enum.min()
  end

  def go() do
    filename = "input.txt"
    IO.puts "[Part 1]"
    IO.puts part1(filename)
    IO.puts "[Part 2]"
    IO.puts part2(filename)
  end
end
