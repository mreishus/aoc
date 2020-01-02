defmodule ElixirDay18.DuetVM do
  alias ElixirDay18.DuetVM

  defstruct [
    :memory,
    :pc,
    :registers,
    :sounds_played,
    :recovered
  ]

  # Registers - Character version 97
  # def init_registers() do
  #   Enum.to_list(?a..?z)
  #   |> Map.new(fn letter -> {letter, 0} end)
  # end

  # Registers - String version "a"
  def init_registers() do
    Enum.to_list(?a..?z)
    |> List.to_string()
    |> String.graphemes()
    |> Map.new(fn letter -> {letter, 0} end)
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

  def new(filename) do
    %DuetVM{
      memory: parse(filename),
      pc: 0,
      registers: init_registers(),
      sounds_played: [],
      recovered: nil
    }
  end

  def lookup(_, arg) when is_integer(arg), do: arg

  def lookup(vm, arg) when is_binary(arg) do
    vm.registers |> Map.get(arg)
  end

  def execute_until_recover(vm) do
    vm = execute_step(vm)

    if vm.recovered == nil do
      execute_until_recover(vm)
    else
      vm.recovered
    end
  end

  def execute_step(%DuetVM{memory: memory, pc: pc} = vm) do
    instruction = memory |> Enum.at(pc)
    do_execute_step(vm, instruction)
  end

  def do_execute_step(vm, ["set", arg1, arg2]) do
    registers = Map.put(vm.registers, arg1, lookup(vm, arg2))
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["add", arg1, arg2]) do
    registers = Map.update!(vm.registers, arg1, fn x -> x + lookup(vm, arg2) end)
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["mul", arg1, arg2]) do
    registers = Map.update!(vm.registers, arg1, fn x -> x * lookup(vm, arg2) end)
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["mod", arg1, arg2]) do
    registers = Map.update!(vm.registers, arg1, fn x -> rem(x, lookup(vm, arg2)) end)
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["snd", arg1]) do
    val = Map.get(vm.registers, arg1)
    sounds_played = vm.sounds_played ++ [val]
    %{vm | sounds_played: sounds_played, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["rcv", arg1]) do
    val = Map.get(vm.registers, arg1)

    if val == 0 do
      %{vm | pc: vm.pc + 1}
    else
      last_sound = vm.sounds_played |> List.last()
      %{vm | recovered: last_sound, pc: vm.pc + 1}
    end
  end

  def do_execute_step(vm, ["jgz", arg1, arg2]) do
    val1 = lookup(vm, arg1)
    val2 = lookup(vm, arg2)

    if val1 > 0 do
      %{vm | pc: vm.pc + val2}
    else
      %{vm | pc: vm.pc + 1}
    end
  end

  def do_execute_step(vm, _) do
    %{vm | pc: vm.pc + 1}
  end
end
