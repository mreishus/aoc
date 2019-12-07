defmodule ElixirDay07Test do
  use ExUnit.Case
  doctest ElixirDay07

  alias ElixirDay07.Computer

  test "day 5 part1" do
    got =
      ElixirDay07.parse("../../05/input.txt")
      |> Computer.solve([1])

    want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5_821_753]
    assert got == want
  end

  test "day 5 part2" do
    got =
      ElixirDay07.parse("../../05/input.txt")
      |> Computer.solve([5])

    want = [11_956_381]
    assert got == want
  end

  test "8_1" do
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    assert Computer.solve(program, [7]) == [0]
    assert Computer.solve(program, [8]) == [1]
    assert Computer.solve(program, [9]) == [0]
  end

  test "8_2" do
    program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    assert Computer.solve(program, [7]) == [1]
    assert Computer.solve(program, [8]) == [0]
    assert Computer.solve(program, [9]) == [0]
  end

  test "8_3" do
    program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    assert Computer.solve(program, [7]) == [0]
    assert Computer.solve(program, [8]) == [1]
    assert Computer.solve(program, [9]) == [0]
  end

  test "8_4" do
    program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    assert Computer.solve(program, [7]) == [1]
    assert Computer.solve(program, [8]) == [0]
    assert Computer.solve(program, [9]) == [0]
  end

  test "jump_1" do
    program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    assert Computer.solve(program, [0]) == [0]
    assert Computer.solve(program, [10]) == [1]
  end

  test "jump_2" do
    program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    assert Computer.solve(program, [0]) == [0]
    assert Computer.solve(program, [10]) == [1]
  end

  test "larger" do
    program = [
      3,
      21,
      1008,
      21,
      8,
      20,
      1005,
      20,
      22,
      107,
      8,
      21,
      20,
      1006,
      20,
      31,
      1106,
      0,
      36,
      98,
      0,
      0,
      1002,
      21,
      125,
      20,
      4,
      20,
      1105,
      1,
      46,
      104,
      999,
      1105,
      1,
      46,
      1101,
      1000,
      1,
      20,
      4,
      20,
      1105,
      1,
      46,
      98,
      99
    ]

    assert Computer.solve(program, [2]) == [999]
    assert Computer.solve(program, [8]) == [1000]
    assert Computer.solve(program, [12]) == [1001]
  end
end
