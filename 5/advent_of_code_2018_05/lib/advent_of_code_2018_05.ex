defmodule AdventOfCode201805 do
  @moduledoc """
  Documentation for AdventOfCode201805.
  """

  @doc """
  Hello world.

  ## Examples

      iex> AdventOfCode201805.hello()
      :world

  """

  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  def file_to_polymer(filename) do
    read_file(filename)
      |> List.first()
      |> String.graphemes()
  end

  def go(filename \\ "input_small.txt") do
    polymer = file_to_polymer(filename)
    IO.inspect polymer
    1
  end

end
