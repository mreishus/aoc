defmodule Elixir2020.Day08.Computer do
  alias Elixir2020.Day08.Computer

  defstruct [
    :program,
    :pc,
    :pc_seen,
    :pc_max,
    :acc
  ]

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

  def step(%Computer{pc: pc, program: program} = c) do
    {op, val} = program |> Map.get(pc)

    c
    |> remember_pc()
    |> do_step({op, val})
  end

  def remember_pc(%Computer{pc: pc, pc_seen: pc_seen} = c) do
    %Computer{c | pc_seen: pc_seen |> MapSet.put(pc)}
  end

  def do_step(%Computer{pc: pc} = c, {"nop", _}) do
    %Computer{c | pc: pc + 1}
  end

  def do_step(%Computer{pc: pc, acc: acc} = c, {"acc", val}) do
    %Computer{c | pc: pc + 1, acc: acc + val}
  end

  def do_step(%Computer{pc: pc} = c, {"jmp", val}) do
    %Computer{c | pc: pc + val}
  end
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
    "Not implemented yet"
  end
end
