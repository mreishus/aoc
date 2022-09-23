defmodule Elixir2021.Day07 do
  def parse(filename) do
    File.stream!(filename)
    |> Enum.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def median([]), do: nil

  def median(list) do
    len = length(list)
    sorted = Enum.sort(list)
    mid = div(len, 2)

    if rem(len, 2) == 0,
      do: (Enum.at(sorted, mid - 1) + Enum.at(sorted, mid)) / 2,
      else: Enum.at(sorted, mid)
  end

  def cost1(index, nums) do
    nums
    |> Enum.map(fn num ->
      abs(num - index)
    end)
    |> Enum.sum()
  end

  def cost2(index, nums) do
    nums
    |> Enum.map(fn num ->
      diff = abs(num - index)
      floor(diff * (diff + 1) / 2)
    end)
    |> Enum.sum()
  end

  def part1(filename) do
    nums = parse(filename)
    median = median(nums)

    # Candidates for final answer
    [floor(median), ceil(median)]
    |> Enum.map(fn index -> cost1(index, nums) end)
    |> Enum.min()
  end

  def part2(filename) do
    nums = parse(filename)
    avg = Enum.sum(nums) / length(nums)

    # Candidates for final answer
    [floor(avg), ceil(avg)]
    |> Enum.map(fn index -> cost2(index, nums) end)
    |> Enum.min()
  end
end
