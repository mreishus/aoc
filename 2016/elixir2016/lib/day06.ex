defmodule Elixir2016.Day06 do
  def part1(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> pos_letter_map()
    |> decode_repeat()
  end

  def part2(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> pos_letter_map()
    |> decode_repeat_least()
  end

  @doc """
  Returns something like

    0 => %{
      "a" => 1,
      "d" => 2,
        "e" => 3,
        "n" => 2,
        "r" => 2,
        "s" => 2,
        "t" => 2,
        "v" => 2
    },
    1 => %{
      "a" => 3,
        "d" => 1,
        "e" => 2,
        "n" => 2,
        "r" => 2,
        "s" => 2,
        "t" => 2,
  etc.
  First key = position in string
  """
  def pos_letter_map(list_of_strings) do
    list_of_strings
    |> Enum.reduce(%{}, fn string, acc ->
      string
      |> String.graphemes()
      |> Stream.with_index()
      |> Enum.reduce(acc, fn {letter, idx}, inner_acc ->
        if Map.has_key?(inner_acc, idx) do
          if Map.has_key?(Map.get(inner_acc, idx), letter) do
            inner_acc |> update_in([idx, letter], fn x -> x + 1 end)
          else
            inner_acc |> put_in([idx, letter], 1)
          end
        else
          inner_acc
          |> Map.put(idx, %{letter => 1})
        end
      end)
    end)
  end

  def decode_repeat(pos_letter_map) do
    pos_letter_map
    |> Map.keys()
    |> Enum.sort()
    |> Enum.map(fn i -> pos_letter_map[i] |> Enum.to_list() end)
    |> Enum.map(fn freq_list ->
      {letter, _freq} = Enum.max_by(freq_list, fn {_letter, freq} -> freq end)
      letter
    end)
    |> Enum.join("")
  end

  def decode_repeat_least(pos_letter_map) do
    pos_letter_map
    |> Map.keys()
    |> Enum.sort()
    |> Enum.map(fn i -> pos_letter_map[i] |> Enum.to_list() end)
    |> Enum.map(fn freq_list ->
      {letter, _freq} = Enum.max_by(freq_list, fn {_letter, freq} -> 0 - freq end)
      letter
    end)
    |> Enum.join("")
  end
end
