defmodule Elixir2016.Day07 do
  def part1(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.filter(&tls?/1)
    |> Enum.count()
  end

  def part2(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.filter(&ssl?/1)
    |> Enum.count()
  end

  ## Removes anything in brackets
  ## Assuming they're never nested
  ## Returns a list of strings
  def remove_hypernet(string) do
    Regex.split(~r/\[.*?\]/, string)
  end

  @doc """
  iex(9)> Elixir2016.Day07.hypernet("abc[def]qwer[asdf]")
  ["def", "asdf"]
  """
  def hypernet(string) do
    Regex.scan(~r/\[(.*?)\]/, string)
    |> Enum.map(fn matchlist -> Enum.at(matchlist, 1) end)
  end

  def tls?(string) do
    abba_outside_hypernet?(string) and not abba_inside_hypernet?(string)
  end

  def abba_inside_hypernet?(string) do
    hypernet(string)
    |> Enum.any?(&abba?/1)
  end

  def abba_outside_hypernet?(string) do
    string
    |> remove_hypernet()
    |> Enum.any?(&abba?/1)
  end

  # Looks for patterns like ABBA or XYYX.  The second char must be diff than the first.
  def abba?(string) do
    Regex.match?(~r/(\w)(?!\1)(\w)\2\1/, string)
  end

  ## Part 2 Stuff 

  @doc """
  iex(1)> "gsg" |> Elixir2016.Day07.aba_list()
  [["g", "s"]]
  iex(2)> "gsg kjk" |> Elixir2016.Day07.aba_list()
  [["g", "s"], ["k", "j"]]
  iex> "zazbzczdzd" |> Elixir2016.Day07.aba_list()
  [["z", "a"], ["z", "b"], ["z", "c"], ["z", "d"], ["d", "z"]]

  Finds a list of all patterns like ABA or XYX in a string.
  ABA would be represented as ["a", "b"].  This makes for easy reversal.
  """
  def aba_list(string) do
    Regex.scan(~r/(\w)(?!\1)(?=(\w)\1)/, string)
    |> Enum.map(fn [_a, b, c] -> [b, c] end)
  end

  @doc """
  Find all ABAs inside and outside the hyerpnet.  If we flip one side,
  are there any matches?  If so, it's SSL.
  """
  def ssl?(string) do
    outside_abas =
      string
      |> remove_hypernet()
      |> Enum.flat_map(&aba_list/1)
      |> Enum.into(MapSet.new())

    inside_abas =
      string
      |> hypernet()
      |> Enum.flat_map(&aba_list/1)
      |> Enum.map(&Enum.reverse/1)
      |> Enum.into(MapSet.new())

    MapSet.intersection(outside_abas, inside_abas)
    |> Enum.any?()
  end
end
