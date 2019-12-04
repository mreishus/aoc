defmodule ElixirDay04 do
  @moduledoc """
  Documentation for ElixirDay04.
  """

  def solve(lower, upper) do
    lower..upper
    |> Stream.filter(&password?/1)
    |> Enum.count()
  end

  def solve2(lower, upper) do
    lower..upper
    |> Stream.filter(&password2?/1)
    |> Enum.count()
  end

  def password?(cand) when cand >= 100_000 and cand <= 999_999 do
    mono_inc?(cand) and part1?(cand)
  end

  def password?(_), do: false

  def password2?(cand) when cand >= 100_000 and cand <= 999_999 do
    mono_inc?(cand) and part2?(cand)
  end

  def password2?(_), do: false

  # Monotonically increasing?
  def mono_inc?(num) do
    Integer.digits(num)
    |> Enum.reduce_while(0, fn x, acc ->
      if x >= acc do
        {:cont, x}
      else
        {:halt, -1}
      end
    end)
    |> Kernel.>=(0)
  end

  # group_lengths(123444) = [1, 1, 1, 3]
  def group_lengths(num) do
    num
    |> Integer.digits()
    |> Enum.chunk_by(& &1)
    |> Enum.map(&length/1)
  end

  # at least one group >= 2
  def part1?(num) do
    group_lengths(num)
    |> Enum.any?(fn x -> x >= 2 end)
  end

  # at least one group == 2
  def part2?(num) do
    group_lengths(num)
    |> Enum.any?(fn x -> x == 2 end)
  end

  def main() do
    solve(245_182, 790_572)
    |> IO.inspect(label: "Part 1")

    solve2(245_182, 790_572)
    |> IO.inspect(label: "Part 2")
  end
end
