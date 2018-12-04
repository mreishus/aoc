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
    file_name = Path.expand("./", __DIR__) |> Path.join("input_small_unsorted.txt")
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  # input: list of unparsed strings
  # output: list of tuples, 0th element is guard number, 1st element is string. "
  # "begin shift" lines are removed
  # example..
  #[
  #    {10, "[1518-11-01 00:05] falls asleep"},
  #    {10, "[1518-11-01 00:25] wakes up"},
  #
  def add_guard([line | lines], guard_num) do
    case Regex.match?(~r/begins shift/, line) do
      true -> add_guard(lines, get_guard(line))
      false -> [ {guard_num, line} | add_guard(lines, guard_num) ]
    end
  end

  def add_guard([], guard_num) do
    []
  end

  # line containing guard number -> guard number
  def get_guard(line) do
    [_, guard_num] = Regex.run(~r/#(\d+)/, line)
    guard_num |> String.to_integer
  end
  # Make this a test
  #line = "[1518-11-01 00:00] Guard #10 begins shift"
  #g = get_guard(line)
  #IO.inspect g

  def go do
    lines = read_file()
      |> Enum.sort()
      |> add_guard(-1)

    IO.puts "[Part 1]: lines"
    IO.inspect lines
  end
end
