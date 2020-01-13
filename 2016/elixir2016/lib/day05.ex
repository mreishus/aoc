defmodule Elixir2016.Day05 do
  def part1(input_str) do
    low = 0
    high = 20_000_000
    # ^ Set this high enough until it works
    # Program is not smart enough to count up until it finds 8 matches.

    passwords =
      low..high
      |> Flow.from_enumerable()
      |> Flow.partition()
      |> Flow.reduce(fn -> %{} end, fn num, acc ->
        pw = pw_test(input_str, num)
        if pw == nil, do: acc, else: Map.put(acc, num, pw)
      end)
      |> Enum.to_list()
      |> Map.new()

    Map.keys(passwords)
    |> Enum.sort()
    |> Enum.take(8)
    |> Enum.map(fn num -> passwords[num] end)
    |> Enum.join("")
    |> String.downcase()
  end

  def part2(input_str) do
    low = 0
    high = 30_000_000
    # ^ Set this high enough until it works
    # Program is not smart enough to count up until it finds 8 matches.

    passwords =
      low..high
      |> Flow.from_enumerable()
      |> Flow.partition()
      |> Flow.reduce(fn -> %{} end, fn num, acc ->
        {pos, pw} = pw2_test(input_str, num)

        if pw == nil do
          acc
        else
          Map.update(acc, pos, [{num, pw}], fn list -> list ++ [{num, pw}] end)
        end
      end)
      |> Enum.to_list()

    # Passwords looks like this:
    # [
    #    {7, [{5708769, "3"}]},
    #    {8, [{5017308, "F"}]},
    #    {4, [{20014135, "7"}]},
    #    {4, [{5357525, "E"}]},
    # Here, position 4 has two values, make sure to take the smaller one

    passwords =
      passwords
      |> Enum.reduce(%{}, fn {pos, [{num, pw}]}, acc ->
        Map.update(acc, pos, {num, pw}, fn {this_num, this_pw} ->
          if num < this_num, do: {num, pw}, else: {this_num, this_pw}
        end)
      end)

    # Passwords looks like this:
    # %{
    #    0 => {13432968, "6"},
    #    1 => {4515059, "9"},
    #    2 => {17743256, "4"},

    Map.keys(passwords)
    |> Enum.sort()
    |> Enum.take(8)
    |> Enum.map(fn pos ->
      {_num, pw} = passwords[pos]
      pw
    end)
    |> Enum.join("")
    |> String.downcase()
  end

  ## MD5 Helper (String -> String)
  def md5(input) do
    :crypto.hash(:md5, input) |> Base.encode16()
  end

  ## Part1 Helpers

  def pw_test(input, num) do
    (input <> Integer.to_string(num))
    |> md5
    |> password
  end

  ## Given an md5 hash, looks for a password
  ## Returns password or nil.
  def password("00000" <> rest) do
    String.at(rest, 0)
  end

  def password(_), do: nil

  ## Part2 Helpers

  def pw2_test(input, num) do
    (input <> Integer.to_string(num))
    |> md5
    |> password2
  end

  def password2("00000" <> rest) do
    pos = String.at(rest, 0)
    char = String.at(rest, 1)

    case Integer.parse(pos) do
      {pos_num, ""} -> {pos_num, char}
      :error -> {nil, nil}
      _ -> {nil, nil}
    end
  end

  def password2(_), do: {nil, nil}
end
