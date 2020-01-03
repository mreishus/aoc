defmodule ElixirDay18.DuetVM_V2 do
  alias ElixirDay18.DuetVM_V2

  defstruct [
    :memory,
    :pc,
    :registers,
    :sounds_played,
    :partner_pid,
    :times_sent,
    :timed_out,
    :program_id
  ]

  def init_and_wait_for_partner(filename, program_id) do
    spawn(fn ->
      vm =
        new(filename)
        |> set_program_id(program_id)

      receive do
        {:partner, pid} ->
          "VM #{program_id}: Got partner, starting.." |> IO.inspect()

          vm
          |> set_partner(pid)
          |> execute_until_timeout()
      end
    end)
  end

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
    %DuetVM_V2{
      memory: parse(filename),
      pc: 0,
      registers: init_registers(),
      sounds_played: [],
      times_sent: 0,
      timed_out: false,
      program_id: nil
    }
  end

  def set_program_id(vm, id) do
    registers = Map.put(vm.registers, "p", id)
    %{vm | registers: registers, program_id: id}
  end

  def set_partner(vm, pid) do
    %{vm | partner_pid: pid}
  end

  def lookup(_, arg) when is_integer(arg), do: arg

  def lookup(vm, arg) when is_binary(arg) do
    vm.registers |> Map.get(arg)
  end

  def execute_until_timeout(vm) do
    vm = execute_step(vm)

    if vm.timed_out == true do
      "VM #{vm.program_id}: Timed out.  Times sent: #{vm.times_sent}" |> IO.inspect()
      vm
    else
      execute_until_timeout(vm)
    end
  end

  def execute_step(%DuetVM_V2{memory: memory, pc: pc} = vm) do
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
    send(vm.partner_pid, {:value, val})
    %{vm | pc: vm.pc + 1, times_sent: vm.times_sent + 1}
  end

  def do_execute_step(vm, ["rcv", arg1]) do
    receive do
      {:value, val} ->
        registers = Map.put(vm.registers, arg1, val)
        %{vm | registers: registers, pc: vm.pc + 1}
    after
      200 ->
        "Recieve timed out" |> IO.inspect()
        %{vm | timed_out: true}
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
