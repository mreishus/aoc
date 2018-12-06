defmodule AdventOfCode201805 do
  @moduledoc """
  Documentation for AdventOfCode201805.
  """
  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  @doc """
    iex> AdventOfCode201805.file_to_polymer("input_small.txt")
    ["d", "a", "b", "A", "c", "C", "a", "C", "B", "A", "c", "C", "c", "a", "D", "A"]
  """
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
