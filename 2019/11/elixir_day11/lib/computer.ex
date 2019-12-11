defmodule ElixirDay11.Computer do
  defstruct [
    :memory,
    :pc,
    :relative_base,
    :inputs,
    :outputs,
    :halted,
    :waiting_for_input
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

  alias ElixirDay11.Computer

  def solve(memory, inputs) when is_list(memory) and is_list(inputs) do
    Computer.new(memory, inputs)
    |> Computer.execute()
    |> Computer.outputs()
  end

  def new(memory, inputs) when is_list(memory) and is_list(inputs) do
    %Computer{
      # Hackish 'unlimited memory'
      memory: Array.from_list(memory ++ List.duplicate(0, 10000)),
      inputs: inputs,
      outputs: [],
      pc: 0,
      relative_base: 0,
      halted: false,
      waiting_for_input: false
    }
  end

  def add_input(%Computer{inputs: inputs} = c, input) do
    new_inputs = inputs ++ [input]
    %Computer{c | inputs: new_inputs}
  end

  # Get the direct value of the memory address of the Nth arg, or PC + N
  def direct(%Computer{pc: pc, memory: memory}, n) do
    Array.get(memory, pc + n)
  end

  # Get the dereferenced value of the Nth arg, after checking the Nth mode of the current instruction.
  def lookup(%Computer{pc: pc, memory: memory, relative_base: relative_base} = computer, n) do
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

  def lookup_left(%Computer{pc: pc, memory: memory, relative_base: relative_base} = computer, n) do
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

  def halted?(%Computer{} = c) do
    c.halted
  end

  def outputs(%Computer{outputs: outputs}), do: outputs

  @doc """
  pop_output/1: Return the oldest output, and a computer with that output removed from it
  pop_output(computer) = {oldest_output, new_computer}
  or
  pop_output(computer) = {nil, computer} # If no outputs
  """
  def pop_output(%Computer{outputs: []} = c), do: {nil, c}

  def pop_output(%Computer{outputs: outputs} = c) do
    [this_output | rest_outputs] = outputs
    new_c = %Computer{c | outputs: rest_outputs}
    {this_output, new_c}
  end

  def execute_step(%Computer{pc: pc, memory: memory} = c) do
    instruction = Array.get(memory, pc) |> rem(100)
    do_execute_step(c, instruction)
  end

  # ADD: 3 = 1 + 2
  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_add) do
    result = lookup(c, 1) + lookup(c, 2)
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  # MULT: 3 = 1 * 2
  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_mult) do
    result = lookup(c, 1) * lookup(c, 2)
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  # SAVE: 1 = Input (No Inputs)
  def do_execute_step(%Computer{inputs: []} = c, @op_save) do
    %Computer{c | waiting_for_input: true}
  end

  # SAVE: 1 = Input (Inputs Exist)
  def do_execute_step(%Computer{pc: pc, memory: memory, inputs: inputs} = c, @op_save) do
    [this_input | new_inputs] = inputs
    new_memory = Array.set(memory, lookup_left(c, 1), this_input)
    new_pc = pc + 2
    %Computer{c | memory: new_memory, pc: new_pc, inputs: new_inputs, waiting_for_input: false}
  end

  # WRITE: Output = 1
  def do_execute_step(%Computer{pc: pc, outputs: outputs} = c, @op_write) do
    this_output = lookup(c, 1)
    new_outputs = outputs ++ [this_output]
    new_pc = pc + 2
    %Computer{c | pc: new_pc, outputs: new_outputs}
  end

  # HALT: Stop
  def do_execute_step(c, @op_halt) do
    %Computer{c | halted: true}
  end

  def do_execute_step(%Computer{pc: pc} = c, @op_jump_if_true) do
    new_pc =
      if lookup(c, 1) != 0 do
        lookup(c, 2)
      else
        pc + 3
      end

    %Computer{c | pc: new_pc}
  end

  def do_execute_step(%Computer{pc: pc} = c, @op_jump_if_false) do
    new_pc =
      if lookup(c, 1) == 0 do
        lookup(c, 2)
      else
        pc + 3
      end

    %Computer{c | pc: new_pc}
  end

  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_less_than) do
    result = if lookup(c, 1) < lookup(c, 2), do: 1, else: 0
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_equals) do
    result = if lookup(c, 1) == lookup(c, 2), do: 1, else: 0
    new_memory = Array.set(memory, lookup_left(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  def do_execute_step(%Computer{pc: pc, relative_base: relative_base} = c, @op_set_rel_base) do
    adjustment = lookup(c, 1)
    new_relative_base = relative_base + adjustment

    new_pc = pc + 2
    %Computer{c | pc: new_pc, relative_base: new_relative_base}
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
