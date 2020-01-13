defmodule Elixir2016.Day09 do
  def part1(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
    |> List.first()
    |> expand()
    |> String.length()
  end

  def expand(string) do
    do_expand("", string)
  end

  @doc """
  iex(8)> Regex.run(~r/\((\d+)x(\d+)\)/, "abcd(3x3)defJKL(4x5)lkqwjerlkqj", return: :index)
  [{4, 5}, {5, 1}, {7, 1}]
  iex(9)> Regex.run(~r/\((\d+)x(\d+)\)/, "abcd(3x3)defJKL(4x5)lkqwjerlkqj")
  ["(3x3)", "3", "3"]

  In this case, we found the first "(3x3)".  
  start - 4     Where the (3x3) starts.
  len - 5       Length of the "(3x3)" sequence itself.
  rep_len - 3   How many of the following characters will be repeated.
  rep_times - 3 How many times they will be repeated

  "abcd(3x3)defJKL(4x5)lkqwjerlkqj"
   \--/     \-/
   begin    repeated
               \-----------------/
                   rest

  We return:  begin <> repeated <> expand(rest).

  "prepend" exists so we can use tail recursion.
  Without tail recursion, it'd simply return:  prepend <> begin <> expand(rest)
  """
  def do_expand(prepend, string) do
    find_marker = ~r/\((\d+)x(\d+)\)/

    case Regex.run(find_marker, string, return: :index) do
      nil ->
        prepend <> string

      [{start, len} | _] ->
        begin = string |> String.slice(0, start)

        [_, rep_len, rep_times] = Regex.run(find_marker, string)
        rep_len = String.to_integer(rep_len)
        rep_times = String.to_integer(rep_times)

        repeated = string |> String.slice(start + len, rep_len) |> String.duplicate(rep_times)
        rest = string |> String.slice(start + len + rep_len, String.length(string))

        do_expand(prepend <> begin <> repeated, rest)
    end
  end
end
