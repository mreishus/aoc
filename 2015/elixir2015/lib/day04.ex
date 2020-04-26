defmodule Elixir2015.Day04 do
  def parse() do
    File.read!("../inputs/04/input.txt")
    |> String.trim()
  end

  @doc """
  If given input = "abcdef", and target prefix = "00000", this
  function will compute md5 hashes like so:

  md5("abcdef1") = ...
  md5("abcdef2") = ...
  md5("abcdef3") = ...
  md5("abcdef4") = ...

  It will return the first N value where the hash generated starts
  with the target prefix.  In this case,

  md5("abcdef609043") = "000001dbbfa..."
       ^     ^           ^
       input |           target prefix
             n returned

  So, helper("abcdef", "000000") = 609043
  """
  def helper(input, target_prefix) do
    1..100_000_000
    |> Enum.reduce_while(nil, fn n, acc ->
      hash =
        (input <> Integer.to_string(n))
        |> md5

      if String.starts_with?(hash, target_prefix) do
        {:halt, n}
      else
        {:cont, acc}
      end
    end)
  end

  @doc """
  This is the same as helper(), but it uses Flow to run in parallel.
  Unfortunately, I don't know how to make this stop searching as soon
  as it finds one answer.  You have to give it an upper bound of
  the search, and it will always search up to there, potentially doing
  extra work, but only returning the first result.

  If you know how to fix this, please let me know.
  """
  def helper_parallel(input, target_prefix, high) do
    low = 1

    # high = 10_000_000

    low..high
    |> Flow.from_enumerable()
    |> Flow.partition()
    |> Flow.reduce(fn -> %{} end, fn num, acc ->
      hash = (input <> Integer.to_string(num)) |> md5

      if String.starts_with?(hash, target_prefix) do
        Map.put(acc, num, hash)
      else
        acc
      end
    end)
    |> Enum.to_list()
    |> Map.new()
    |> Map.keys()
    |> List.first()
  end

  def part1() do
    # Serial Version
    # parse()
    # |> helper("00000")

    # Parallel Version
    # (Faster, but I have to specify the upper bound of search,
    # which I don't really like)
    parse()
    |> helper_parallel("00000", 500_000)
  end

  def part2() do
    # Serial Version
    # parse()
    # |> helper("000000")

    # Parallel Version
    # (Faster, but I have to specify the upper bound of search,
    # which I don't really like)
    parse()
    |> helper_parallel("000000", 10_000_000)
  end

  ## MD5 Helper (String -> String)
  def md5(input) do
    :crypto.hash(:md5, input) |> Base.encode16(case: :lower)
  end
end
