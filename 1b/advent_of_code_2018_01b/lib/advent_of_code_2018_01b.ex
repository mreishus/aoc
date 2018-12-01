defmodule AdventOfCode201801b do
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
    sum_strings_with_operator: Meant to be passed to a Enum.reduce call.
   
    Param 1: string_with_operator (string) formatted like "+1" or "-10".  Sign is mandatory.
    Param 2: sum (integer) Rolling sum.
  """
  def sum_strings_with_operator(string_with_operator, sum) do
    [operator, num_string] = String.split(string_with_operator, "", parts: 2, trim: true)
    {num, ""} = Integer.parse(num_string)
    case operator do
      "-" -> sum - num
      "+" -> sum + num
      _ -> sum + num
    end
  end

  @doc """
    compute_input_sum: Reads all lines in input.txt, sums them, and prints the
    sum to console.
  """
  def compute_input_sum() do
    file_name = Path.expand("./", __DIR__) |> Path.join("input.txt")
    file_sum = File.stream!(file_name)
      |> Stream.map(&String.trim/1)
      |> Enum.reduce(0, &AdventOfCode201801b.sum_strings_with_operator/2)

    IO.puts file_sum 
  end

end

