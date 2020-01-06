defmodule ElixirDay23 do
  alias ElixirDay23.VM

  def main do
    "Main" |> IO.inspect()

    vm =
      VM.new("../input.txt")
      |> VM.execute_until_halt()

    vm.mul_count |> IO.inspect(label: "Part 1")

    "Part 2?" |> IO.inspect()

    vm =
      VM.new("../input.txt")
      |> VM.turn_off_debug()
      |> VM.execute_until_halt()

    vm |> IO.inspect()
    # 500: Too low.
  end
end
