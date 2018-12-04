defmodule AdventOfCode201804 do
  @moduledoc """
  Documentation for AdventOfCode201804.
  """

  @doc """
  Hello world.

  ## Examples

      iex> AdventOfCode201804.hello()
      :world

  """
  def hello do
    :world
  end

  def read_file() do
    file_name = Path.expand("./", __DIR__) |> Path.join("input_small.txt")
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  def go do
    lines = read_file()
    IO.puts "[Part 1]: lines"
    IO.inspect files
  end
end
