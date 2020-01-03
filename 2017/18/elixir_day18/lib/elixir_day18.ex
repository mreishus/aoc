defmodule ElixirDay18 do
  alias ElixirDay18.{DuetVM, DuetVM_V2}

  def main do
    DuetVM.new("../input.txt")
    |> DuetVM.execute_until_recover()
    |> IO.inspect(label: "Part 1")

    # vm0 = DuetVM_V2.init_and_wait_for_partner("../input_small2.txt", 0)
    # vm1 = DuetVM_V2.init_and_wait_for_partner("../input_small2.txt", 1)
    vm0 = DuetVM_V2.init_and_wait_for_partner("../input.txt", 0)
    vm1 = DuetVM_V2.init_and_wait_for_partner("../input.txt", 1)
    send(vm1, {:partner, vm0})
    send(vm0, {:partner, vm1})
    Process.sleep(1 * 1000)
  end
end
