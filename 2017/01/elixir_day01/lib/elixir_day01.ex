defmodule ElixirDay01 do
  @moduledoc """
  Documentation for ElixirDay01.
  """

  def main do
    {:ok, contents} = File.read("../input.txt")

    contents = String.trim(contents)
    IO.puts("Part 1:")
    IO.puts(part1(contents))
    IO.puts("Part 2:")
    IO.puts(part2(contents))
  end

  def part1(nums) do
    captcha(nums, 1)
  end

  def part2(nums) do
    rotate_amount = (String.length(nums) / 2) |> round()
    captcha(nums, rotate_amount)
  end

  def captcha(nums, rotate_amount) do
    s1 = nums |> String.graphemes()
    s2 = nums |> rotate_string(rotate_amount) |> String.graphemes()

    s1
    |> Enum.zip(s2)
    |> Enum.filter(fn {first, second} -> first == second end)
    |> Enum.map(fn {first, _second} ->
      {first_int, ""} = Integer.parse(first)
      first_int
    end)
    |> Enum.sum()
  end

  def rotate_string(input, num) do
    input
    |> to_charlist()
    |> rotate_charlist(num)
    |> to_string()
  end

  def rotate_charlist(input, 0), do: input

  def rotate_charlist([h | tl], num) when num > 0 do
    rotate_charlist(tl ++ [h], num - 1)
  end
end
