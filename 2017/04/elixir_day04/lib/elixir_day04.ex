defmodule ElixirDay04 do
  @moduledoc """
  Documentation for ElixirDay04.
  """

  @doc """
  Hello world.

  ## Examples

      iex> ElixirDay04.hello()
      :world

  """
  def hello do
    :world
  end

  def main do
    IO.puts("part 1")

    File.stream!("../input.txt")
    |> Stream.filter(&valid_passphrase?/1)
    |> Enum.count()
    |> IO.puts()

    IO.puts("part 2")

    File.stream!("../input.txt")
    |> Stream.filter(&valid_passphrase_p2?/1)
    |> Enum.count()
    |> IO.puts()
  end

  def valid_passphrase?(str) do
    words =
      str
      |> String.split(~r/\s+/)

    Enum.uniq(words) == words
  end

  def valid_passphrase_p2?(str) do
    words =
      str
      |> String.split(~r/\s+/)
      |> Enum.map(&String.graphemes/1)
      |> Enum.map(&Enum.sort/1)

    Enum.uniq(words) == words
  end
end
