defmodule Elixir2016.Day16 do
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
  end

  @doc """
  iex(3)> Day16.expand("111100001010")
  "1111000010100101011110000"
  """
  def expand(string_a) do
    string_b =
      string_a
      |> String.reverse()
      |> String.replace("0", "2")
      |> String.replace("1", "0")
      |> String.replace("2", "1")

    [string_a, "0", string_b] |> IO.iodata_to_binary()
  end

  @doc """
  iex(24)> Day16.expand_length("10000", 20)                    
  "10000011110010000111"
  iex(23)> Day16.expand_length("10000", 20) |> Day16.checksum()                       
  "01100"
  """
  def expand_length(string_a, l) do
    if length(String.graphemes(string_a)) < l do
      expand_length(expand(string_a), l)
    else
      string_a |> String.slice(0, l)
    end
  end

  @doc """
  iex(15)> Day16.checksum("110010110100")
  "100"
  """
  def checksum(string_a) do
    answer =
      string_a
      |> String.graphemes()
      |> Enum.chunk_every(2)
      |> Enum.reduce([], fn [c1, c2], acc ->
        if c1 == c2 do
          ["1" | acc]
        else
          ["0" | acc]
        end
      end)
      |> Enum.reverse()
      |> IO.iodata_to_binary()

    if rem(length(answer |> String.graphemes()), 2) == 0 do
      checksum(answer)
    else
      answer
    end
  end

  def part1(filename) do
    parse(filename)
    |> expand_length(272)
    |> checksum()
  end

  def part2(filename) do
    parse(filename)
    |> expand_length(35_651_584)
    |> checksum()
  end
end
