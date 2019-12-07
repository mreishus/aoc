defmodule ElixirDay07 do
  @moduledoc """
  Documentation for ElixirDay07.
  """
  alias ElixirDay07.{Computer, ComputerServer}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def permutations([]), do: [[]]

  def permutations(list),
    do: for(elem <- list, rest <- permutations(list -- [elem]), do: [elem | rest])

  def amplify_once_max_seq(program) when is_list(program) do
    permutations([0, 1, 2, 3, 4])
    |> Enum.map(fn phase_sequence ->
      value = amplify_once(program, phase_sequence)
      {phase_sequence, value}
    end)
    |> Enum.max_by(fn {_phase_sequence, value} ->
      value
    end)
  end

  def amplify_once(program, phase_sequence) when is_list(program) and is_list(phase_sequence) do
    phase_sequence
    |> Enum.map(fn phase ->
      {:ok, pid} = ComputerServer.start(program, [phase])
      pid
    end)
    |> Enum.reduce(0, fn pid, acc ->
      ComputerServer.add_input(pid, acc)
      ComputerServer.pop_output(pid)
    end)
  end

  def main do
    parse("../input.txt")
    |> amplify_once_max_seq()
    |> IO.inspect(label: "day 5 part1")
  end
end
