defmodule ElixirDay07.ComputerServer do
  use GenServer

  alias ElixirDay07.{Computer}

  @doc """
  start/2: Start a new genserver.  Provide it an intcode program to run, with
  some inputs.  It'll start executing immediately.

  program: a list of ints (intcode) to run
  input: a list of ints to feed to the computer as input, provide empty list if none
  """
  def start(program, input) when is_list(program) and is_list(input) do
    GenServer.start(__MODULE__, {program, input})
  end

  @doc """
  outputs/1: Get the current list of outputs.  Does not modify.
  """
  def outputs(pid) do
    GenServer.call(pid, :outputs)
  end

  @doc """
  pop_output/1: Return the oldest output from the computer.
  As a side effect, remove it from the computer's list of outputs.
  """
  def pop_output(pid) do
    GenServer.call(pid, :pop_output)
  end

  @doc """
  add_input/1: Feed an input to the computer.  It will continue executing
  if able.
  """
  def add_input(pid, input) do
    GenServer.call(pid, {:add_input, input})
  end

  def halted?(pid) do
    GenServer.call(pid, :halted?)
  end

  #########

  def init({program, input}) when is_list(program) and is_list(input) do
    # Note: This forces the caller of init to wait for the 
    # program to finish executing (they're blocked). Can be fixed
    # by having the GenServer send an execute() message to itself.
    c = Computer.new(program, input) |> Computer.execute()
    {:ok, c}
  end

  def handle_call(:outputs, _from, state) do
    {:reply, Computer.outputs(state), state}
  end

  def handle_call(:pop_output, _from, state) do
    {output, new_state} = Computer.pop_output(state)
    {:reply, output, new_state}
  end

  def handle_call(:halted?, _from, state) do
    {:reply, Computer.halted?(state), state}
  end

  def handle_call({:add_input, input}, _from, state) do
    new_state =
      state
      |> Computer.add_input(input)
      |> Computer.execute()

    {:reply, :ok, new_state}
  end
end
