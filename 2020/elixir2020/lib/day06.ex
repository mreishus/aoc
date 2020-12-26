defmodule Elixir2020.Day06 do
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.split("\n\n")
    |> Enum.map(fn lines ->
      lines
      |> String.split()
      |> Enum.map(&String.graphemes/1)
      |> Enum.map(&MapSet.new/1)
    end)
  end

  def part1(filename) do
    parse(filename)
    |> Enum.map(fn sets ->
      sets
      |> Enum.reduce(&MapSet.union/2)
      |> Enum.count()
    end)
    |> Enum.sum()
  end

  def part2(filename) do
    parse(filename)
    |> Enum.map(fn sets ->
      sets
      |> Enum.reduce(&MapSet.intersection/2)
      |> Enum.count()
    end)
    |> Enum.sum()
  end
end
