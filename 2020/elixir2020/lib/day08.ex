defmodule Elixir2020.Day08.Computer do
  alias Elixir2020.Day08.Computer

  defstruct [
    :program,
    :pc,
    :pc_seen,
    :pc_max,
    :acc
  ]

  ## new/1: Given a program, create a new computer.
  def new(program) when is_list(program) do
    pc_max = length(program) - 1

    ## Turn program into a map with the instruction numbers as keys
    ## I'd like to use {:array, github: "jfacorro/elixir-array"}, but I can't since
    ## it requires elixir 1.11.1, and arch only has .0 right now..
    ## Cannot use list because it's O(n) to access inside of it.

    program = program |> Enum.with_index(0) |> Enum.map(fn {k, v} -> {v, k} end) |> Map.new()

    %Computer{
      program: program,
      pc_max: pc_max,
      pc: 0,
      pc_seen: MapSet.new(),
      acc: 0
    }
  end

  ## execute/1: Given a computer, run the program until either a termination or infinite loop is detected.
  def execute(%Computer{pc: pc, pc_seen: pc_seen, pc_max: pc_max, acc: acc} = c) do
    cond do
      pc >= pc_max ->
        {:halted, acc}

      MapSet.member?(pc_seen, pc) ->
        {:infinite_loop, acc}

      true ->
        c |> step() |> execute()
    end
  end

  ## step/1: Given a computer, run one instruction.
  def step(%Computer{pc: pc, program: program} = c) do
    {op, val} = program |> Map.get(pc)

    c
    |> remember_pc()
    |> do_step({op, val})
  end

  ## remember_pc/1: Given a computer, put the current program counter (pc) in the pc_seen set.
  def remember_pc(%Computer{pc: pc, pc_seen: pc_seen} = c) do
    %Computer{c | pc_seen: pc_seen |> MapSet.put(pc)}
  end

  ## do_step/2 (cpu, {"nop", _}): Advance the PC by one.
  def do_step(%Computer{pc: pc} = c, {"nop", _}) do
    %Computer{c | pc: pc + 1}
  end

  ## do_step/2 (cpu, {"acc", val}): Advance the PC by one and the accumulator by val.
  def do_step(%Computer{pc: pc, acc: acc} = c, {"acc", val}) do
    %Computer{c | pc: pc + 1, acc: acc + val}
  end

  ## do_step/2 (cpu, {"jmp", val}): Advance the PC by val.
  def do_step(%Computer{pc: pc} = c, {"jmp", val}) do
    %Computer{c | pc: pc + val}
  end

  ## find_corruption/1: Look for which instruction needs to be flipped to stop infinite loops
  ## from occuring, then return the "acc" value after terminating.
  def find_corruption(%Computer{} = c) do
    case flippable?(c) do
      false ->
        c |> step() |> find_corruption()

      true ->
        ## Branch and try flipped computer
        {state, acc} = c |> flip() |> execute()

        if state == :halted do
          ## It halted, we're done!
          acc
        else
          ## Continue on as normal and try flipping the next
          ## flippable.
          c |> step() |> find_corruption()
        end
    end
  end

  ## flippable?/1 Given a computer, is the next operation to be run flippable?
  def flippable?(%Computer{pc: pc, program: program}) do
    {op, _} = program |> Map.get(pc)
    flip_op(op) != nil
  end

  ## flip/1 Given a computer with the next instruction set to "jmp" or "nop",
  ## return that computer an updated program that flips that instruction (jmp becomes nop,
  ## nop becomes jmp.)
  def flip(%Computer{pc: pc, program: program} = c) do
    {op, val} = program |> Map.get(pc)
    %Computer{c | program: Map.put(program, pc, {flip_op(op), val})}
  end

  ## flip_op/1 Given an op that can be flipped, return the flipped version.
  ## Given any other op, return nil.
  def flip_op("jmp"), do: "nop"
  def flip_op("nop"), do: "jmp"
  def flip_op(_), do: nil
end

defmodule Elixir2020.Day08 do
  alias Elixir2020.Day08.Computer

  def parse() do
    File.stream!("../inputs/08/input.txt")
    |> Stream.map(&String.trim/1)
    |> Enum.map(fn x ->
      [op, val] = String.split(x)
      {op, String.to_integer(val)}
    end)
  end

  def part1() do
    parse()
    |> Computer.new()
    |> Computer.execute()
  end

  def part2() do
    parse()
    |> Computer.new()
    |> Computer.find_corruption()
  end
end
