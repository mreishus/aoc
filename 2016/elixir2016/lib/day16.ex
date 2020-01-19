# Array:
# 14.59user 2.18system 0:16.31elapsed 102%CPU (0avgtext+0avgdata 9743080maxresident)k
# String:
# 54.68user 8.36system 1:02.86elapsed 100%CPU (0avgtext+0avgdata 11317384maxresident)k

defmodule Elixir2016.Day16 do
  alias Elixir2016.Day16Array
  # alias Elixir2016.Day16String
  def part1(filename) do
    Day16Array.part1(filename)
  end

  def part2(filename) do
    Day16Array.part2(filename)
  end
end

## Array based implementation (faster)
defmodule Elixir2016.Day16Array do
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.graphemes()
    |> Enum.map(fn x ->
      case x do
        "0" -> 0
        "1" -> 1
        true -> raise "Can't parse"
      end
    end)
  end

  def expand(list_a) do
    list_b =
      list_a
      |> Enum.reverse()
      |> Enum.map(fn x ->
        if x == 1 do
          0
        else
          1
        end
      end)

    Enum.concat([list_a, [0], list_b])
  end

  def expand_length(list_a, l) do
    if length(list_a) < l do
      expand_length(expand(list_a), l)
    else
      list_a |> Enum.take(l)
    end
  end

  def checksum(list_a) do
    answer =
      list_a
      |> Enum.chunk_every(2)
      |> Enum.reduce([], fn [c1, c2], acc ->
        if c1 == c2 do
          [1 | acc]
        else
          [0 | acc]
        end
      end)
      |> Enum.reverse()

    if rem(length(answer), 2) == 0 do
      checksum(answer)
    else
      answer
    end
  end

  def list_to_string(list_a) do
    list_a
    |> Enum.map(&Integer.to_string/1)
    |> Enum.join("")
  end

  def part1(filename) do
    parse(filename)
    |> expand_length(272)
    |> checksum()
    |> list_to_string()
  end

  def part2(filename) do
    parse(filename)
    |> expand_length(35_651_584)
    |> checksum()
    |> list_to_string()
  end
end

## String based implementation (Slower)
defmodule Elixir2016.Day16String do
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
