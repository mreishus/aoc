## Just for fun, I'm including the optimizations I did that
## were too slow to actually solve the problem.
## Read from bottom up to see the optimizations as I added them.
defmodule ElixirDay23.VMFailedOptimizations do
  alias ElixirDay23.{VM, PrimeFactors}

  defstruct [
    :memory,
    :pc,
    :registers,
    :mul_count,
    :halted
  ]

  def init_registers() do
    Enum.to_list(?a..?h)
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
    %VM{
      memory: parse(filename),
      pc: 0,
      registers: init_registers(),
      mul_count: 0,
      halted: false
    }
  end

  def turn_off_debug(vm) do
    registers = Map.put(vm.registers, "a", 1)
    %{vm | registers: registers}
  end

  def lookup(_, arg) when is_integer(arg), do: arg

  def lookup(vm, arg) when is_binary(arg) do
    vm.registers |> Map.get(arg)
  end

  def execute_until_halt(vm) do
    vm = execute_step(vm)

    if vm.halted == true do
      vm
    else
      execute_until_halt(vm)
    end
  end

  def execute_step(%VM{memory: memory, pc: pc} = vm) do
    instruction = memory |> Enum.at(pc)

    [
      vm.registers["a"],
      vm.registers["b"],
      vm.registers["c"],
      vm.registers["d"],
      vm.registers["e"],
      vm.registers["f"],
      vm.registers["g"],
      vm.registers["h"]
    ]
    |> IO.inspect()

    [pc + 1 | instruction] |> IO.inspect()
    IO.puts("")

    do_execute_step(vm, instruction)
  end

  ## Optimization of outer loop - Do both loops inside elixir.
  ## Too slow.  At this point I realize what it's actually doing and
  ## change to a better prime check.
  def do_execute_step(%VM{pc: 9, registers: r} = vm, _instruction) do
    this_b = r["b"]

    outer_test_pass =
      2..this_b
      |> Enum.reduce_while(false, fn this_d, acc_outer ->
        this_d |> IO.inspect()

        test_pass =
          2..this_b
          |> Enum.reduce_while(false, fn this_e, acc ->
            if this_d * this_e == this_b do
              {:halt, true}
            else
              {:cont, false}
            end
          end)

        if test_pass do
          {:halt, true}
        else
          {:cont, false}
        end
      end)

    new_f = if outer_test_pass == true, do: 0, else: 1

    new_reg =
      vm.registers
      |> Map.put("f", new_f)

    %{vm | registers: new_reg, pc: 24}
  end

  ## Optimization of outer loop - Exit loop early if we set f = 0,
  ## No need to continue looping.  Works well except those cases
  ## where we never set f = 0 (prime numbers)
  def do_execute_step(%VM{pc: 20, registers: r} = vm, instruction) do
    # instruction: ["sub", "d", -1]

    target = r["b"] - 1

    new_d =
      if r["f"] == 0 and r["d"] < target do
        target
      else
        r["d"] + 1
      end

    new_reg =
      vm.registers
      |> Map.put("d", new_d)

    %{vm | registers: new_reg, pc: 21}
  end

  ## Optimization of inner loop - Do loop inside elixir
  def do_execute_step(%VM{pc: 10, registers: r} = vm, _instruction) do
    test_pass =
      2..r["b"]
      |> Enum.reduce_while(false, fn this_e, acc ->
        if r["d"] * this_e == r["b"] do
          {:halt, true}
        else
          {:cont, false}
        end
      end)

    new_f = if test_pass == true, do: 0, else: r["f"]
    new_e = r["b"] - 1

    new_reg =
      vm.registers
      |> Map.put("f", new_f)
      |> Map.put("e", new_e)

    %{vm | registers: new_reg, pc: 19}
  end

  ## Optimization of inner loop - Still loop, but
  ## Group together instructions
  def do_execute_step(%VM{pc: 11, registers: r} = vm, _instruction) do
    zero_test = r["d"] * r["e"] - r["b"]
    new_f = if zero_test == 0, do: 0, else: r["f"]
    new_e = r["e"] + 1
    new_g = new_e - r["b"]

    new_reg =
      vm.registers
      |> Map.put("f", new_f)
      |> Map.put("e", new_e)
      |> Map.put("g", new_g)

    %{vm | registers: new_reg, pc: 19}
    # "special instruction" |> IO.inspect()
    # instruction |> IO.inspect()
  end

  def do_execute_step(vm, ["set", arg1, arg2]) do
    registers = Map.put(vm.registers, arg1, lookup(vm, arg2))
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["sub", arg1, arg2]) do
    registers = Map.update!(vm.registers, arg1, fn x -> x - lookup(vm, arg2) end)
    %{vm | registers: registers, pc: vm.pc + 1}
  end

  def do_execute_step(vm, ["mul", arg1, arg2]) do
    registers = Map.update!(vm.registers, arg1, fn x -> x * lookup(vm, arg2) end)
    %{vm | registers: registers, pc: vm.pc + 1, mul_count: vm.mul_count + 1}
  end

  def do_execute_step(vm, ["jnz", arg1, arg2]) do
    val1 = lookup(vm, arg1)
    val2 = lookup(vm, arg2)

    if val1 != 0 do
      %{vm | pc: vm.pc + val2}
    else
      %{vm | pc: vm.pc + 1}
    end
  end

  # Nil instruction = halted
  def do_execute_step(vm, nil) do
    %{vm | halted: true}
  end
end
