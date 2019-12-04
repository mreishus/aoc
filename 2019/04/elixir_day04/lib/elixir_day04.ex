defmodule ElixirDay04 do
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

  def password?(num), do: six_digit?(num) and mono_inc?(num) and part1?(num)
  def password2?(num), do: six_digit?(num) and mono_inc?(num) and part2?(num)

  def six_digit?(num) when is_integer(num) and num >= 100_000 and num <= 999_999, do: true
  def six_digit?(_), do: false

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
