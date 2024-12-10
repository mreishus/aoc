defmodule Elixir2024.Day01 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.split/1)
    |> Stream.map(fn [a, b] -> {String.to_integer(a), String.to_integer(b)} end)
    |> Enum.unzip()
  end

  def part1(filename) do
    {list1, list2} = parse(filename)

    Enum.zip(Enum.sort(list1), Enum.sort(list2))
    |> Enum.map(fn {a, b} -> abs(b - a) end)
    |> Enum.sum()
  end

  def part2(filename) do
    {list1, list2} = parse(filename)
    list2freqs = Enum.frequencies(list2)

    list1
    |> Enum.map(fn x -> x * Map.get(list2freqs, x, 0) end)
    |> Enum.sum()
  end
end
