defmodule Elixir2021.Day01 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.to_integer/1)
  end

  def increase_count(nums, window) do
    nums
    |> Enum.zip(Enum.drop(nums, window))
    |> Enum.reduce(0, fn {a, b}, acc ->
      if b > a, do: acc + 1, else: acc
    end)
  end

  def part1(filename) do
    parse(filename)
    |> increase_count(1)
  end

  def part2(filename) do
    parse(filename)
    |> increase_count(3)
  end
end
