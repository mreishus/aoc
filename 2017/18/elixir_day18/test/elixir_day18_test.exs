defmodule ElixirDay18Test do
  use ExUnit.Case
  doctest ElixirDay18
  alias ElixirDay18.DuetVM

  test "Part 1 example" do
    got =
      DuetVM.new("../input_small.txt")
      |> DuetVM.execute_until_recover()

    want = 4
    assert got == want
  end

  test "Part 1" do
    got =
      DuetVM.new("../input.txt")
      |> DuetVM.execute_until_recover()

    want = 9423
    assert got == want
  end
end
