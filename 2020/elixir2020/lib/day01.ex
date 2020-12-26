defmodule Elixir2020.Day01 do
  def parse(filename) do
    File.stream!("../inputs/01/input.txt")
    |> Stream.map(&String.trim/1)
    |> Enum.map(&String.to_integer/1)
  end

  @doc """
  three_sum(list, target) 
    Looks for 2 numbers in list that when added, return target.
    If found, returns the product of those numbers (a * b).
    If not found, returns nil.
  """
  def two_sum(list, target) do
    all_nums = list |> Map.new(fn x -> {x, 1} end)

    case do_two_sum(all_nums, list, target) do
      nil -> nil
      {a, b} -> a * b
    end
  end

  defp do_two_sum(_all_nums_map, [], _target), do: nil

  defp do_two_sum(all_nums_map, [this_num | rest_list], target) do
    look_for_num = target - this_num

    if Map.has_key?(all_nums_map, look_for_num) do
      {this_num, look_for_num}
    else
      do_two_sum(all_nums_map, rest_list, target)
    end
  end

  @doc """
  three_sum(list, target) 
    Looks for 3 numbers in list that when added, return target.
    If found, returns the product of those numbers (a * b * c).
    If not found, returns nil.
  """
  def three_sum([], _target), do: nil

  def three_sum([this_num | rest_list], target) do
    case two_sum(rest_list, target - this_num) do
      nil ->
        three_sum(rest_list, target)

      ab ->
        ab * this_num
    end
  end

  def part1(filename) do
    filename
    |> parse()
    |> two_sum(2020)
  end

  def part2(filename) do
    filename
    |> parse()
    |> three_sum(2020)
  end
end
