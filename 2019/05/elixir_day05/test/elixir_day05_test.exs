defmodule ElixirDay05Test do
  use ExUnit.Case
  doctest ElixirDay05

  alias ElixirDay05.Computer

  test "part1" do
    got =
      ElixirDay05.parse("../input.txt")
      |> Computer.solve([1])

    want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5_821_753]
    assert got == want
  end

  test "8_1" do
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    assert Computer.solve(program, [7]) == [0]
    assert Computer.solve(program, [8]) == [1]
    assert Computer.solve(program, [9]) == [0]
  end
end
