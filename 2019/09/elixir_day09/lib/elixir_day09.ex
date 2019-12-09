defmodule ElixirDay09 do
  @moduledoc """
  Documentation for ElixirDay09.
  """
  alias ElixirDay09.{ComputerServer}

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

  @doc """
  Given a program, try all permutations of [0, 1, 2, 3, 4],
  to see which phase sequence generates the highest value
  when passed through amplify_once.
  """
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

  @doc """
  Given a program and a phase sequence, run the program through 5 chained computers.
  The phase sequence is a list of 5 inputs, like, [3, 2, 4, 1, 5].  These are fed
  to each computer as the first input.

  0 -> A -> B -> C -> D -> E -> Output.
  """
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

  @doc """
  Given a program, try all permutations of [5, 6, 7, 8 9],
  to see which phase sequence generates the highest value
  when passed through amplify_loop.
  """
  def amplify_loop_max_seq(program) when is_list(program) do
    permutations([5, 6, 7, 8, 9])
    |> Enum.map(fn phase_sequence ->
      value = amplify_loop(program, phase_sequence)
      {phase_sequence, value}
    end)
    |> Enum.max_by(fn {_phase_sequence, value} ->
      value
    end)
  end

  @doc """
  Given a program and a phase sequence, run the program through 5 chained computers,
  with feedback.
  The phase sequence is a list of 5 inputs, like, [3, 2, 4, 1, 5].  These are fed
  to each computer as the first input.

  0 -> A -> B -> C -> D -> E -> Output.
       ^                   v
       \    <-   <-  <-    /

  The feedback stops once all computers have halted.
  """
  def amplify_loop(program, phase_sequence) when is_list(program) and is_list(phase_sequence) do
    # Start 5 computers
    pids =
      phase_sequence
      |> Enum.map(fn phase ->
        {:ok, pid} = ComputerServer.start(program, [phase])
        pid
      end)

    # Loop through the computers, feeding them the last computer's output as their next input.
    # Starts with initial input "0", and tracks the number of halted computers,
    # stops when all of them have halted.  Assumes they will all halt in order, directly
    # one after another.
    pids
    |> Stream.cycle()
    |> Enum.reduce_while(%{input: 0, halt_count: 0}, fn pid, acc ->
      %{input: input, halt_count: halt_count} = acc
      ComputerServer.add_input(pid, input)
      output = ComputerServer.pop_output(pid)

      halt_count = halt_count + if ComputerServer.halted?(pid), do: 1, else: 0

      if halt_count == length(phase_sequence) do
        {:halt, output}
      else
        {:cont, %{input: output, halt_count: halt_count}}
      end
    end)
  end

  def main do
    parse("../../07/input.txt")
    |> amplify_once_max_seq()
    |> IO.inspect(label: "day 7 part1")

    parse("../../07/input.txt")
    |> amplify_loop_max_seq()
    |> IO.inspect(label: "day 7 part2")
  end
end
