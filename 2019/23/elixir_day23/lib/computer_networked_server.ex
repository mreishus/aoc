defmodule ElixirDay23.ComputerNWServer do
  use GenServer

  alias ElixirDay23.{ComputerNW}

  @doc """
  start/2: Start a new genserver.  Provide it an intcode program to run, with
  some inputs.  It'll start executing immediately.

  program: a list of ints (intcode) to run
  input: a list of ints to feed to the computer as input, provide empty list if none
  """
  def start(program, input, coordinator_pid) when is_list(program) and is_list(input) do
    GenServer.start(__MODULE__, {program, input, coordinator_pid})
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

  def add_two_input(pid, input1, input2) do
    GenServer.call(pid, {:add_two_input, input1, input2})
  end

  def halted?(pid) do
    GenServer.call(pid, :halted?)
  end

  #########

  def init({program, input, coordinator_pid}) when is_list(program) and is_list(input) do
    # Note: This forces the caller of init to wait for the 
    # program to finish executing (they're blocked). Can be fixed
    # by having the GenServer send an execute() message to itself.
    # c = ComputerNW.new(program, input) |> ComputerNW.execute()
    c = ComputerNW.new(program, input, coordinator_pid) |> ComputerNW.execute()
    # 10ms
    schedule_tick(10)
    {:ok, c}
  end

  defp schedule_tick(interval) do
    Process.send_after(self(), :tick, interval)
  end

  def handle_info(:tick, state) do
    # "Tick" |> IO.inspect()

    # state |> IO.inspect()

    new_state =
      if state.waiting_for_input do
        # "TIck add" |> IO.inspect()

        state
        |> ComputerNW.add_input(-1)
        |> ComputerNW.execute()
      else
        state
      end

    schedule_tick(10)
    {:noreply, new_state}
  end

  def handle_call(:outputs, _from, state) do
    {:reply, ComputerNW.outputs(state), state}
  end

  def handle_call(:pop_output, _from, state) do
    {output, new_state} = ComputerNW.pop_output(state)
    {:reply, output, new_state}
  end

  def handle_call(:halted?, _from, state) do
    {:reply, ComputerNW.halted?(state), state}
  end

  def handle_call({:add_input, input}, _from, state) do
    new_state =
      state
      |> ComputerNW.add_input(input)
      |> ComputerNW.execute()

    {:reply, :ok, new_state}
  end

  def handle_call({:add_two_input, input1, input2}, _from, state) do
    new_state =
      state
      |> ComputerNW.add_input(input1)
      |> ComputerNW.add_input(input2)
      |> ComputerNW.execute()

    {:reply, :ok, new_state}
  end
end
