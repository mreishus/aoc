defmodule Elixir2016.Day12 do
  alias Elixir2016.Day12.BunnyVM

  def part1(filename) do
    parse(filename)
    |> BunnyVM.new()
    |> BunnyVM.execute_till_halt()
  end

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.split/1)
    |> Enum.map(fn list ->
      list |> Enum.map(&try_parse_int/1)
    end)
  end

  def try_parse_int(string) do
    case Integer.parse(string) do
      :error -> string
      {num, _} -> num
    end
  end
end

defmodule Elixir2016.Day12.BunnyVM do
  alias Elixir2016.Day12.BunnyVM

  defstruct [
    :memory,
    :pc,
    :registers,
    :halted
  ]

  def init_registers() do
    Enum.to_list(?a..?d)
    |> List.to_string()
    |> String.graphemes()
    |> Map.new(fn letter -> {letter, 0} end)
  end

  def new(memory) do
    %BunnyVM{
      memory: memory,
      pc: 0,
      registers: init_registers(),
      halted: false
    }
  end

  def lookup(_, arg) when is_integer(arg), do: arg

  def lookup(vm, arg) when is_binary(arg) do
    vm.registers |> Map.get(arg)
  end

  def execute_till_halt(vm) do
    vm = execute_step(vm)

    if vm.halted == true do
      vm
    else
      execute_till_halt(vm)
    end
  end

  def execute_step(%BunnyVM{memory: memory, pc: pc} = vm) do
    instruction = memory |> Enum.at(pc)

    if instruction != nil do
      do_execute_step(vm, instruction)
    else
      %{vm | halted: true}
    end
  end

  def do_execute_step(vm, ["cpy", arg1, arg2]) do
    registers = Map.put(vm.registers, arg2, lookup(vm, arg1))
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["inc", arg1]) do
    registers = Map.update!(vm.registers, arg1, fn x -> x + 1 end)
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["dec", arg1]) do
    registers = Map.update!(vm.registers, arg1, fn x -> x - 1 end)
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["jnz", arg1, arg2]) do
    arg1 = lookup(vm, arg1)
    arg2 = lookup(vm, arg2)

    if arg1 != 0 do
      %{vm | pc: vm.pc + arg2}
    else
      %{vm | pc: vm.pc + 1}
    end
  end
end
