defmodule ElixirDay07.Computer do
  defstruct [
    :memory,
    :pc,
    :inputs,
    :outputs,
    :halted
  ]

  @op_add 1
  @op_mult 2
  @op_save 3
  @op_write 4
  @op_jump_if_true 5
  @op_jump_if_false 6
  @op_less_than 7
  @op_equals 8
  @op_halt 99

  @mode_position 0
  @mode_immediate 1

  alias ElixirDay07.Computer

  def solve(memory, inputs) when is_list(memory) and is_list(inputs) do
    Computer.new(memory, inputs)
    |> Computer.execute()
    |> Computer.outputs()
  end

  def new(memory, inputs) when is_list(memory) and is_list(inputs) do
    %Computer{
      memory: Array.from_list(memory),
      inputs: inputs,
      outputs: [],
      pc: 0,
      halted: false
    }
  end

  # Get the direct value of the memory address of the Nth arg, or PC + N
  def direct(%Computer{pc: pc, memory: memory}, n) do
    Array.get(memory, pc + n)
  end

  # Get the dereferenced value of the Nth arg, after checking the Nth mode of the current instruction.
  def lookup(%Computer{pc: pc, memory: memory} = computer, n) do
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

      _ ->
        raise "Unknown mode"
    end
  end

  def execute(computer) do
    computer = execute_step(computer)

    if computer.halted do
      computer
    else
      execute(computer)
    end
  end

  def outputs(%Computer{outputs: outputs}), do: outputs

  def execute_step(%Computer{pc: pc, memory: memory} = c) do
    instruction = Array.get(memory, pc) |> rem(100)
    do_execute_step(c, instruction)
  end

  # ADD: 3 = 1 + 2
  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_add) do
    result = lookup(c, 1) + lookup(c, 2)
    new_memory = Array.set(memory, direct(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  # MULT: 3 = 1 * 2
  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_mult) do
    result = lookup(c, 1) * lookup(c, 2)
    new_memory = Array.set(memory, direct(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  # SAVE: 1 = Input
  def do_execute_step(%Computer{pc: pc, memory: memory, inputs: inputs} = c, @op_save) do
    [this_input | new_inputs] = inputs
    new_memory = Array.set(memory, direct(c, 1), this_input)
    new_pc = pc + 2
    %Computer{c | memory: new_memory, pc: new_pc, inputs: new_inputs}
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
    new_memory = Array.set(memory, direct(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
  end

  def do_execute_step(%Computer{pc: pc, memory: memory} = c, @op_equals) do
    result = if lookup(c, 1) == lookup(c, 2), do: 1, else: 0
    new_memory = Array.set(memory, direct(c, 3), result)
    new_pc = pc + 4
    %Computer{c | memory: new_memory, pc: new_pc}
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
