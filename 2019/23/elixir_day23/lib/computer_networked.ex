defmodule ElixirDay23.ComputerNW do
  defstruct [
    :memory,
    :pc,
    :relative_base,
    :inputs,
    :outputs,
    :halted,
    :waiting_for_input,
    :coordinator_pid
  ]

  @op_add 1
  @op_mult 2
  @op_save 3
  @op_write 4
  @op_jump_if_true 5
  @op_jump_if_false 6
  @op_less_than 7
  @op_equals 8
  @op_set_rel_base 9
  @op_halt 99

  @mode_position 0
  @mode_immediate 1
  @mode_relative 2

  alias ElixirDay23.{ComputerNW, Coordinator}

  def send_to_network(%ComputerNW{coordinator_pid: coordinator_pid}, three_packet_list) do
    Coordinator.send_packet(coordinator_pid, three_packet_list)
  end

  # def solve(memory, inputs, ???) when is_list(memory) and is_list(inputs) do
  #   ComputerNW.new(memory, inputs, ???)
  #   |> ComputerNW.execute()
  #   |> ComputerNW.outputs()
  # end

  def new(memory, inputs, coordinator_pid) when is_list(memory) and is_list(inputs) do
    %ComputerNW{
      # Hackish 'unlimited memory'
      memory: Array.from_list(memory ++ List.duplicate(0, 10000)),
      inputs: inputs,
      outputs: [],
      pc: 0,
      relative_base: 0,
      halted: false,
      waiting_for_input: false,
      coordinator_pid: coordinator_pid
    }
  end

  def add_input(%ComputerNW{inputs: inputs} = c, input) do
    new_inputs = inputs ++ [input]
    %ComputerNW{c | inputs: new_inputs}
  end

  # Get the direct value of the memory address of the Nth arg, or PC + N
  def direct(%ComputerNW{pc: pc, memory: memory}, n) do
    Array.get(memory, pc + n)
  end

  # Get the dereferenced value of the Nth arg, after checking the Nth mode of the current instruction.
  def lookup(%ComputerNW{pc: pc, memory: memory, relative_base: relative_base} = computer, n) do
    raw_instruction = Array.get(memory, pc)
    # If instruction is 105, and n=1, mode is the "1", or the 2nd digit
    # from right 0 indexed (3rd when counting naturally)
    mode = digit_from_right(raw_instruction, n + 1)

    case mode do
      @mode_position ->
        position = direct(computer, n)
        Array.get(memory, position)

      @mode_immediate ->
        direct(computer, n)

      @mode_relative ->
        position = direct(computer, n) + relative_base
        Array.get(memory, position)

      _ ->
        raise "Unknown mode"
    end
  end

  def lookup_left(%ComputerNW{pc: pc, memory: memory, relative_base: relative_base} = computer, n) do
    raw_instruction = Array.get(memory, pc)
    # If instruction is 105, and n=1, mode is the "1", or the 2nd digit
    # from right 0 indexed (3rd when counting naturally)
    mode = digit_from_right(raw_instruction, n + 1)

    case mode do
      @mode_position ->
        direct(computer, n)

      @mode_immediate ->
        direct(computer, n)

      @mode_relative ->
        direct(computer, n) + relative_base

      _ ->
        raise "Unknown mode"
    end
  end

  def execute(computer) do
    computer = execute_step(computer)

    if computer.halted or (computer.waiting_for_input and length(computer.inputs) == 0) do
      computer
    else
      execute(computer)
    end
  end

  def halted?(%ComputerNW{} = c) do
    c.halted
  end

  def outputs(%ComputerNW{outputs: outputs}), do: outputs

  def set_memory(%ComputerNW{memory: memory} = c, index, value) do
    new_memory = Array.set(memory, index, value)
    %ComputerNW{c | memory: new_memory}
  end

  def has_output?(%ComputerNW{outputs: []}), do: false
  def has_output?(%ComputerNW{}), do: true

  @doc """
  pop_output/1: Return the oldest output, and a computer with that output removed from it
  pop_output(computer) = {oldest_output, new_computer}
  or
  pop_output(computer) = {nil, computer} # If no outputs
  """
  def pop_output(%ComputerNW{outputs: []} = c), do: {nil, c}

  def pop_output(%ComputerNW{outputs: outputs} = c) do
    [this_output | rest_outputs] = outputs
    new_c = %ComputerNW{c | outputs: rest_outputs}
    {this_output, new_c}
  end

  def execute_step(%ComputerNW{pc: pc, memory: memory} = c) do
    instruction = Array.get(memory, pc) |> rem(100)
    do_execute_step(c, instruction)
  end

  # ADD: 3 = 1 + 2
  def do_execute_step(%ComputerNW{pc: pc, memory: memory} = c, @op_add) do
    result = lookup(c, 1) + lookup(c, 2)
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %ComputerNW{c | memory: new_memory, pc: new_pc}
  end

  # MULT: 3 = 1 * 2
  def do_execute_step(%ComputerNW{pc: pc, memory: memory} = c, @op_mult) do
    result = lookup(c, 1) * lookup(c, 2)
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %ComputerNW{c | memory: new_memory, pc: new_pc}
  end

  # SAVE: 1 = Input (No Inputs)
  def do_execute_step(
        %ComputerNW{pc: pc, memory: memory, inputs: [], coordinator_pid: coordinator_pid} = c,
        @op_save
      ) do
    # Network CHANGE: If no input exists,
    # Don't block, Ask the coordinator for an input

    # don't block, use -1
    [this_input | new_inputs] = Coordinator.get_packet(coordinator_pid)

    new_memory = Array.set(memory, lookup_left(c, 1), this_input)
    new_pc = pc + 2
    %ComputerNW{c | memory: new_memory, pc: new_pc, inputs: new_inputs, waiting_for_input: false}
  end

  # SAVE: 1 = Input (No Inputs)
  def do_execute_step(%ComputerNW{inputs: []} = c, @op_save) do
    %ComputerNW{c | waiting_for_input: true}
  end

  # SAVE: 1 = Input (Inputs Exist)
  def do_execute_step(%ComputerNW{pc: pc, memory: memory, inputs: inputs} = c, @op_save) do
    [this_input | new_inputs] = inputs

    # "Input exists" |> IO.inspect()
    # this_input |> IO.inspect(label: "this_input")

    new_memory = Array.set(memory, lookup_left(c, 1), this_input)
    new_pc = pc + 2
    %ComputerNW{c | memory: new_memory, pc: new_pc, inputs: new_inputs, waiting_for_input: false}
  end

  # WRITE: Output = 1
  def do_execute_step(%ComputerNW{pc: pc, outputs: outputs} = c, @op_write) do
    this_output = lookup(c, 1)
    new_outputs = outputs ++ [this_output]

    # Network CHANGE:  If New_outputs has 3 values,
    # We send them to the network and remove them from the output buffer
    new_outputs =
      if length(new_outputs) == 3 do
        send_to_network(c, new_outputs)
        []
      else
        new_outputs
      end

    new_pc = pc + 2
    %ComputerNW{c | pc: new_pc, outputs: new_outputs}
  end

  # HALT: Stop
  def do_execute_step(c, @op_halt) do
    %ComputerNW{c | halted: true}
  end

  def do_execute_step(%ComputerNW{pc: pc} = c, @op_jump_if_true) do
    new_pc =
      if lookup(c, 1) != 0 do
        lookup(c, 2)
      else
        pc + 3
      end

    %ComputerNW{c | pc: new_pc}
  end

  def do_execute_step(%ComputerNW{pc: pc} = c, @op_jump_if_false) do
    new_pc =
      if lookup(c, 1) == 0 do
        lookup(c, 2)
      else
        pc + 3
      end

    %ComputerNW{c | pc: new_pc}
  end

  def do_execute_step(%ComputerNW{pc: pc, memory: memory} = c, @op_less_than) do
    result = if lookup(c, 1) < lookup(c, 2), do: 1, else: 0
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %ComputerNW{c | memory: new_memory, pc: new_pc}
  end

  def do_execute_step(%ComputerNW{pc: pc, memory: memory} = c, @op_equals) do
    result = if lookup(c, 1) == lookup(c, 2), do: 1, else: 0
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %ComputerNW{c | memory: new_memory, pc: new_pc}
  end

  def do_execute_step(%ComputerNW{pc: pc, relative_base: relative_base} = c, @op_set_rel_base) do
    adjustment = lookup(c, 1)
    new_relative_base = relative_base + adjustment

    new_pc = pc + 2
    %ComputerNW{c | pc: new_pc, relative_base: new_relative_base}
  end

  def do_execute_step(_, opcode) do
    raise "Unknown opcode " <> Integer.to_string(opcode)
  end

  def digit_from_right(x, n) do
    x
    |> Integer.floor_div(round(:math.pow(10, n)))
    |> rem(10)
  end
end
