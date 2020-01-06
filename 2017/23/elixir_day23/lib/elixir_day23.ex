defmodule ElixirDay23 do
  alias ElixirDay23.VM

  def main do
    "Main" |> IO.inspect()

    vm =
      VM.new("../input.txt")
      |> VM.execute_until_halt()

    vm.mul_count |> IO.inspect(label: "Part 1")
  end
end
