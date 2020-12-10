defmodule Elixir2020.Day05 do
  # Parse file into:
  # [
  #   {"BFBFBBB", "RLL"},
  #   {"BFFBBBB", "RRR"},
  #   {"FFBBFBF", "LLL"},
  #   ...
  # ]
  def parse() do
    File.stream!("../inputs/05/input.txt")
    |> Enum.map(&String.trim/1)
    |> Enum.map(fn s -> String.split_at(s, 7) end)
  end

  def get_row({bf_string, _lr_string}), do: decode_binary(bf_string, "B")
  def get_column({_bf_string, lr_string}), do: decode_binary(lr_string, "R")

  def get_id(pair), do: get_row(pair) * 8 + get_column(pair)

  def decode_binary(input, high_char) do
    input
    |> String.graphemes()
    |> Enum.reduce(0, fn x, acc ->
      acc = acc * 2

      if x == high_char do
        acc + 1
      else
        acc
      end
    end)
  end

  def find_missing(set, to_check) do
    if MapSet.member?(set, to_check) do
      find_missing(set, to_check + 1)
    else
      to_check
    end
  end

  def part1() do
    parse()
    |> Enum.max_by(&get_id/1)
    |> get_id()
  end

  def part2() do
    all_ids =
      parse()
      |> Enum.map(&get_id/1)
      |> MapSet.new()

    find_missing(all_ids, Enum.min(all_ids))
  end
end
