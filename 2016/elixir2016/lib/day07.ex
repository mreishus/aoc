defmodule Elixir2016.Day07 do
  def part1(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.filter(&tls?/1)
    |> Enum.count()
  end

  ## Removes anything in brackets
  ## Assuming they're never nested
  ## Replacing with Z - working as a makeshift "split" here, so we
  ## don't detect abbas across brackets
  def remove_hypernet(string) do
    Regex.replace(~r/\[.*?\]/, string, "Z")
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
    |> abba?()
  end

  def abba?(string) do
    Regex.match?(~r/(\w)(?!\1)(\w)\2\1/, string)
  end
end
