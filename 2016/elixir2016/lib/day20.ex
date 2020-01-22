defmodule Elixir2016.Day20 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse_line/1)
    |> Enum.sort_by(fn {low, _high} -> low end)
    |> Enum.to_list()
  end

  def parse_line(line) do
    [low, high] = line |> String.split("-") |> Enum.map(&String.to_integer/1)
    {low, high}
  end

  def part1(filename) do
    parse(filename)
    |> lowest_available()
  end

  def part2(filename) do
    parse(filename)
    |> count_available()
  end

  @doc """
  blacklist_list example
   [
    {0, 2793737},
    {2162802, 8327007},
    {2663526, 7317845},
    {2793738, 2841656},
    {2841657, 3867364},
    {3867365, 5819500},
    ...
  ]

  Finds the first unblocked IP.
  """
  def lowest_available(blacklist_list) do
    blacklist_list
    |> Enum.reduce_while(0, fn {low, high}, acc ->
      if acc < low do
        {:halt, acc}
      else
        {:cont, high + 1}
      end
    end)
  end

  @doc """
  Finds the # of unblocked IPs, assuming that the highest blocked IP is the 
  top of the range.
  """
  def count_available(blacklist_list) do
    {_, count} =
      blacklist_list
      |> Enum.reduce({0, 0}, fn {low, high}, {acc_marker, acc_count} ->
        new_mark = max(acc_marker, high + 1)

        if acc_marker < low do
          {new_mark, acc_count + (low - acc_marker)}
        else
          {new_mark, acc_count}
        end
      end)

    count
  end
end
