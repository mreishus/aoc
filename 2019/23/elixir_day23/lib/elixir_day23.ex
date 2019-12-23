defmodule ElixirDay23 do
  @moduledoc """
  Documentation for ElixirDay23.
  """
  alias ElixirDay23.{Breakout, Coordinator}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  @doc """
  That's not the right answer; your answer is too high. If you're stuck, make
  sure you're using the full input data; there are also some general tips on the
  about page, or you can ask for hints on the subreddit. Please wait one minute
  before trying again. (You guessed 30757.) [Return to Day 23]
  """
  def main do
    program = parse("../../23/input.txt")
    how_many = 50

    {ok, pid} = Coordinator.start(program, how_many)

    pid
    |> IO.inspect(label: "coordinator pid")
  end

  # This might need to be moved to test
  def old_main do
    parse("../../13/input.txt")
    |> Breakout.part1()
    |> IO.inspect(label: "Day 13, Part 1: ")

    parse("../../13/input.txt")
    |> Breakout.part2()
    |> IO.inspect(label: "Day 13, Part 2: ")
  end
end
