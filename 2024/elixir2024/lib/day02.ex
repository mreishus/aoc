defmodule Elixir2024.Day02 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.reject(&(&1 == ""))
    |> Stream.map(&String.split/1)
    |> Stream.map(fn items ->
      items |> Enum.map(&String.to_integer/1)
    end)
    |> Enum.to_list()
  end

  def get_deltas(list) do
    Enum.zip(tl(list), list)
    |> Enum.map(fn {a, b} -> a - b end)
  end

  def is_safe(list) do
    deltas = get_deltas(list)

    magnitude_correct = Enum.all?(deltas, fn d -> 0 <= abs(d) && abs(d) <= 3 end)
    monotonic = Enum.all?(deltas, fn d -> d > 0 end) || Enum.all?(deltas, fn d -> d < 0 end)

    magnitude_correct && monotonic
  end

  def is_safe_allow_one_removal(list) do
    if is_safe(list) do
      true
    else
      0..(length(list) - 1)
      |> Enum.any?(fn i ->
        list
        |> List.delete_at(i)
        |> is_safe()
      end)
    end
  end

  def part1(filename) do
    parse(filename)
    |> Enum.filter(&is_safe/1)
    |> Enum.count()
  end

  def part2(filename) do
    parse(filename)
    |> Enum.filter(&is_safe_allow_one_removal/1)
    |> Enum.count()
  end
end
