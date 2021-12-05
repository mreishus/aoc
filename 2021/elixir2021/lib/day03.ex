defmodule Elixir2021.Day03 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
  end

  @doc """
  Get the bit length by looking at the first line of the input.
  If nums = ["01010", "01010", "01010", "01010", .. ],
  then return 4 (the 0-indexed length).
  """
  def bit_len(nums), do: String.length(Enum.at(nums, 0)) - 1

  def part1(filename) do
    nums = parse(filename)

    0..bit_len(nums)
    |> Enum.reduce(["", ""], fn i, [common, rare] ->
      if most_common_at(nums, i) == "1" do
        [common <> "1", rare <> "0"]
      else
        [common <> "0", rare <> "1"]
      end
    end)
    |> Enum.map(&String.to_integer(&1, 2))
    |> Enum.reduce(&Kernel.*/2)
  end

  def part2(filename) do
    nums = parse(filename)
    o2 = bit_criteria_selection(nums, &most_common_at/2)
    co2 = bit_criteria_selection(nums, &least_common_at/2)
    o2 * co2
  end

  def bit_criteria_selection(nums, picker) do
    0..bit_len(nums)
    |> Enum.reduce_while(nums, fn i, nums ->
      target = picker.(nums, i)

      new_nums =
        Enum.filter(nums, fn num ->
          String.at(num, i) == target
        end)

      case length(new_nums) do
        1 -> {:halt, Enum.at(new_nums, 0)}
        _ -> {:cont, new_nums}
      end
    end)
    |> String.to_integer(2)
  end

  def most_common_at(nums, i), do: common_at(nums, i, false)
  def least_common_at(nums, i), do: common_at(nums, i, true)

  @doc """
  Inside string "nums" of "0"s and "1"s, find the most common digit at position i.
  If invert is true, find the least common digit at position i instead.
  """
  def common_at(nums, i, invert) do
    freqs_at_i =
      nums
      |> Enum.map(fn num -> String.at(num, i) end)
      |> Enum.reduce(%{"0" => 0, "1" => 0}, fn x, acc ->
        Map.update(acc, x, 1, &(&1 + 1))
      end)

    if freqs_at_i["1"] >= freqs_at_i["0"] != invert do
      "1"
    else
      "0"
    end
  end
end
