defmodule ElixirDay13Test do
  use ExUnit.Case
  doctest ElixirDay13

  alias ElixirDay13.{Computer, ComputerServer, PainterRobot}

  ## Day 11 specific tests
  test "day11_part1" do
    got =
      ElixirDay13.parse("../../11/input.txt")
      |> PainterRobot.new(0)
      |> PainterRobot.execute()
      |> PainterRobot.count_painted_squares()

    assert got == 2539
  end

  test "day11_part2" do
    got =
      ElixirDay13.parse("../../11/input.txt")
      |> PainterRobot.new(1)
      |> PainterRobot.execute()
      |> PainterRobot.count_painted_squares()

    assert got == 248
  end

  ## Day 9 specific tests
  test "day9_testprog1" do
    test_prog91 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    outputs = Computer.solve(test_prog91, [])
    # Quine
    assert outputs == test_prog91
  end

  test "day9_testprog2" do
    test_prog92 = [1102, 34_915_192, 34_915_192, 7, 4, 7, 99, 0]
    outputs = Computer.solve(test_prog92, [])
    assert outputs == [1_219_070_632_396_864]
  end

  test "day9_testprog3" do
    test_prog93 = [104, 1_125_899_906_842_624, 99]
    outputs = Computer.solve(test_prog93, [])
    assert outputs == [1_125_899_906_842_624]
  end

  test "day9_part1" do
    outputs =
      ElixirDay13.parse("../../09/input.txt")
      |> Computer.solve([1])

    assert outputs == [3_780_860_499]
  end

  test "day9_part2" do
    outputs =
      ElixirDay13.parse("../../09/input.txt")
      |> Computer.solve([2])

    assert outputs == [33343]
  end

  ## Day 7 Specific Tests
  test "day7_part1" do
    {got_seq, got_val} =
      ElixirDay13.parse("../../07/input.txt")
      |> ElixirDay13.Amplify.amplify_once_max_seq()

    assert got_seq == [2, 0, 3, 1, 4]
    assert got_val == 13848
  end

  test "day7_part2" do
    {got_seq, got_val} =
      ElixirDay13.parse("../../07/input.txt")
      |> ElixirDay13.Amplify.amplify_loop_max_seq()

    assert got_seq == [6, 8, 7, 5, 9]
    assert got_val == 12_932_154
  end

  test "amplify_once" do
    prog_a_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]

    prog_a_2 = [
      3,
      23,
      3,
      24,
      1002,
      24,
      10,
      24,
      1002,
      23,
      -1,
      23,
      101,
      5,
      23,
      23,
      1,
      24,
      23,
      23,
      4,
      23,
      99,
      0,
      0
    ]

    prog_a_3 = [
      3,
      31,
      3,
      32,
      1002,
      32,
      10,
      32,
      1001,
      31,
      -2,
      31,
      1007,
      31,
      0,
      33,
      1002,
      33,
      7,
      33,
      1,
      33,
      31,
      31,
      1,
      32,
      31,
      31,
      4,
      31,
      99,
      0,
      0,
      0
    ]

    test_cases = [
      {prog_a_1, [4, 3, 2, 1, 0], 43210},
      {prog_a_2, [0, 1, 2, 3, 4], 54321},
      {prog_a_3, [1, 0, 4, 3, 2], 65210}
    ]

    # Test amplify_once
    test_cases
    |> Enum.each(fn {prog, phase_seq, want_val} ->
      got_val = ElixirDay13.Amplify.amplify_once(prog, phase_seq)
      assert got_val == want_val
    end)

    # Test amplify_once_max_seq
    test_cases
    |> Enum.each(fn {prog, want_seq, want_val} ->
      {got_seq, got_val} = ElixirDay13.Amplify.amplify_once_max_seq(prog)
      assert got_seq == want_seq
      assert got_val == want_val
    end)
  end

  test "amplify_loop" do
    prog_b_1 = [
      3,
      26,
      1001,
      26,
      -4,
      26,
      3,
      27,
      1002,
      27,
      2,
      27,
      1,
      27,
      26,
      27,
      4,
      27,
      1001,
      28,
      -1,
      28,
      1005,
      28,
      6,
      99,
      0,
      0,
      5
    ]

    prog_b_2 = [
      3,
      52,
      1001,
      52,
      -5,
      52,
      3,
      53,
      1,
      52,
      56,
      54,
      1007,
      54,
      5,
      55,
      1005,
      55,
      26,
      1001,
      54,
      -5,
      54,
      1105,
      1,
      12,
      1,
      53,
      54,
      53,
      1008,
      54,
      0,
      55,
      1001,
      55,
      1,
      55,
      2,
      53,
      55,
      53,
      4,
      53,
      1001,
      56,
      -1,
      56,
      1005,
      56,
      6,
      99,
      0,
      0,
      0,
      0,
      10
    ]

    test_cases = [
      {prog_b_1, [9, 8, 7, 6, 5], 139_629_729},
      {prog_b_2, [9, 7, 8, 5, 6], 18216}
    ]

    # Test amplify_loop
    test_cases
    |> Enum.each(fn {prog, phase_seq, want_val} ->
      got_val = ElixirDay13.Amplify.amplify_loop(prog, phase_seq)
      assert got_val == want_val
    end)

    # Test amplify_loop_max_seq
    test_cases
    |> Enum.each(fn {prog, want_seq, want_val} ->
      {got_seq, got_val} = ElixirDay13.Amplify.amplify_loop_max_seq(prog)
      assert got_seq == want_seq
      assert got_val == want_val
    end)
  end

  ## GenServer tests

  test "day 5 part1 GenServer (Full Input)" do
    program = ElixirDay13.parse("../../05/input.txt")
    {:ok, pid} = ComputerServer.start(program, [1])
    got = ComputerServer.outputs(pid)
    want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5_821_753]
    assert got == want
  end

  test "day 5 part1 GenServer (Pass Input after starting)" do
    program = ElixirDay13.parse("../../05/input.txt")
    {:ok, pid} = ComputerServer.start(program, [])
    assert ComputerServer.outputs(pid) == []
    ComputerServer.add_input(pid, 1)
    got = ComputerServer.outputs(pid)
    want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5_821_753]
    assert got == want
  end

  test "day5 part2 GenServer (Pop Output)" do
    program = ElixirDay13.parse("../../05/input.txt")
    {:ok, pid} = ComputerServer.start(program, [5])
    old_output_len = length(ComputerServer.outputs(pid))
    output = ComputerServer.pop_output(pid)
    new_output_len = length(ComputerServer.outputs(pid))
    assert new_output_len + 1 == old_output_len
    assert output == 11_956_381
  end

  ## Non GenServer Tests

  test "pausing on missing input, adding input, and resuming" do
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    c = Computer.new(program, []) |> Computer.execute()
    assert c.waiting_for_input == true
    c = c |> Computer.add_input(8) |> Computer.execute()
    assert c.waiting_for_input == false
    assert c.halted == true
    assert c.outputs == [1]
  end

  test "day 5 part1" do
    got =
      ElixirDay13.parse("../../05/input.txt")
      |> Computer.solve([1])

    want = [0, 0, 0, 0, 0, 0, 0, 0, 0, 5_821_753]
    assert got == want
  end

  test "day 5 part2" do
    got =
      ElixirDay13.parse("../../05/input.txt")
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
