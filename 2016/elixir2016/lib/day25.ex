defmodule Elixir2016.Day25 do
  alias Elixir2016.Day25.BunnyVM

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

  def part1(filename) do
    prog = parse(filename)
    len = 10

    desired_signal =
      Stream.iterate(0, fn x ->
        if x == 0, do: 1, else: 0
      end)
      |> Enum.take(len)

    Stream.iterate(1, fn x -> x + 1 end)
    |> Stream.map(fn x ->
      signal = vm_signal_from_value(prog, x, len)
      {x, signal}
    end)
    |> Stream.filter(fn {_x, signal} ->
      signal == desired_signal
    end)
    |> Enum.take(1)
    |> Enum.map(fn {x, _signal} -> x end)
  end

  def vm_signal_from_value(prog, init_val, len) do
    vm =
      prog
      |> BunnyVM.new()
      |> BunnyVM.register_set("a", init_val)
      |> BunnyVM.execute(len)

    vm.output
  end
end

defmodule Elixir2016.Day25.BunnyVM do
  alias Elixir2016.Day25.BunnyVM

  defstruct [
    :memory,
    :pc,
    :registers,
    :toggled,
    :output
  ]

  def init_registers() do
    Enum.to_list(?a..?d)
    |> List.to_string()
    |> String.graphemes()
    |> Map.new(fn letter -> {letter, 0} end)
  end

  def new(memory) do
    memory_map =
      memory
      |> Enum.with_index()
      |> Enum.map(fn {line, i} -> {i, line} end)
      |> Enum.into(%{})

    %BunnyVM{
      memory: memory_map,
      pc: 0,
      registers: init_registers(),
      toggled: false,
      output: []
    }
  end

  def register_set(vm, reg, value) do
    registers = Map.put(vm.registers, reg, value)
    %{vm | registers: registers}
  end

  def lookup(_, arg) when is_integer(arg), do: arg

  def lookup(vm, arg) when is_binary(arg) do
    vm.registers |> Map.get(arg)
  end

  # Execute until we have `len` number of outputs
  def execute(%BunnyVM{memory: memory, pc: pc} = vm, len) do
    instruction = memory |> Map.get(pc)

    if instruction != nil and length(vm.output) < len do
      # %{pc: pc, i: instruction} |> IO.inspect()
      # %{pc: pc, i: instruction, registers: vm.registers} |> IO.inspect()

      do_execute_step(vm, instruction)
      |> execute(len)
    else
      vm
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

  def do_execute_step(vm, ["out", arg1]) do
    arg1 = lookup(vm, arg1)
    %{vm | pc: vm.pc + 1, output: Enum.concat(vm.output, [arg1])}
  end

  def do_execute_step(vm, ["tgl", arg1]) do
    arg1 = lookup(vm, arg1)
    toggle_idx = vm.pc + arg1

    if Map.has_key?(vm.memory, toggle_idx) do
      # "Toggling index #{toggle_idx}" |> IO.inspect()
      memory = Map.update!(vm.memory, toggle_idx, &toggle_instruction/1)
      %{vm | memory: memory, pc: vm.pc + 1}
    else
      %{vm | pc: vm.pc + 1}
    end
  end

  def toggle_instruction([inst, a, b]) do
    [toggle_instruction(inst), a, b]
  end

  def toggle_instruction([inst, a]) do
    [toggle_instruction(inst), a]
  end

  def toggle_instruction(inst) do
    # For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
    # For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
    case inst do
      ## One
      "inc" -> "dec"
      "dec" -> "inc"
      "tgl" -> "inc"
      ## Two
      "cpy" -> "jnz"
      "jnz" -> "cpy"
    end
  end
end
