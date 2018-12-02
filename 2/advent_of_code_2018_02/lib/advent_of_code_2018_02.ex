defmodule AdventOfCode201802 do
  @moduledoc """
  Documentation for AdventOfCode201802.
  """
  def read_file() do
    file_name = Path.expand("./", __DIR__) |> Path.join("input.txt")
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  def go do
    AdventOfCode201802.Part1.go()
    AdventOfCode201802.Part2.go()
  end
end

defmodule AdventOfCode201802.Part1 do
  import AdventOfCode201802, only: [read_file: 0]

  # Given a string, find a map showing how many times each character is used ("char_counts").
  # input: "hello" 
  # output: %{"h" => 1, "e" => 1, "l" => 2, "o" => 1}
  def get_char_counts(str) do
    str 
      |> String.graphemes
      |> Enum.reduce(%{}, fn(x, acc) -> Map.put(acc, x, (acc[x] || 0) + 1) end)
  end

  # Given a char counts map, and a desired count, are any of the values in that map the desired_count?
  # input: %{"h" => 1, "e" => 1, "l" => 2, "o" => 1}, 2
  # output: true
  # input: %{"h" => 1, "e" => 1, "l" => 2, "o" => 1}, 3
  # output: false
  def char_count_contains_num(char_count, desired_count) do
    char_count
      |> Map.values
      |> Enum.member?(desired_count)
  end

  # Given a string, does it have any character repeated exactly X number of times?
  # input: "hello", 2
  # output: true
  # input: "hello", 3
  # output: false
  def string_has_char_repeated_x_times(str, num), do: 
    get_char_counts(str) |> char_count_contains_num(num)

  # Find the checksum of the file by multiplying the number of strings that have
  # any character repeated 2 times by the number of strings that have any character
  # repeated 3 times.
  def go do
    data = read_file()

    two_count = data 
      |> Enum.filter(fn x -> string_has_char_repeated_x_times(x, 2) end) 
      |> Enum.count
    three_count = data 
      |> Enum.filter(fn x -> string_has_char_repeated_x_times(x, 3) end) 
      |> Enum.count
    IO.puts "[Part1] Checksum is:"
    IO.puts two_count * three_count
  end
end

defmodule AdventOfCode201802.Part2 do
  import AdventOfCode201802, only: [read_file: 0]

  # Given two strings, are they off by only one character?
  # input: "hello", "hallo"
  # output: true
  def is_one_char_off([x | xs], [y | ys]) do
    case x == y do
      true -> is_one_char_off(xs, ys)
      false -> xs == ys
    end
  end
  def is_one_char_off([], []), do: false

  # Given two strings, return a string that consists of only the characters
  # that are the same between the string (position counts).
  # input: "aaabbbccc", "aaZbbZccZ"
  # output: "aabbcc"
  def get_strings_no_diff([{str1, str2}]) do
    str2_array = str2 |> String.graphemes
    str1
      |> String.graphemes
      |> Enum.with_index
      |> Enum.reduce("", fn({letter, index}, acc) ->
          case letter == (str2_array |> Enum.at(index)) do
            true -> acc <> letter
            false -> acc
          end
        end)
  end

  # Go through the file, looking for the first string pair that is off only by one character,
  # then print the string that is common to those.
  def go do
    data = read_file()

    IO.puts ""
    IO.puts "[Part 2]"
    combos = for i <- data, j <- data, is_one_char_off(i |> String.graphemes, j |> String.graphemes), do: {i, j}

    IO.puts combos
     |> Enum.take(1)
     |> get_strings_no_diff()
  end
end
