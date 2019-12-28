defmodule ElixirDay13Test do
  use ExUnit.Case
  doctest ElixirDay13
  alias ElixirDay13.Parse

  test "Parses a file" do
    got = Parse.parse_file("../input_small.txt")

    want = %{
      0 => %{depth: 3, scanner: 0, delta: 1},
      1 => %{depth: 2, scanner: 0, delta: 1},
      4 => %{depth: 4, scanner: 0, delta: 1},
      6 => %{depth: 4, scanner: 0, delta: 1}
    }

    assert got == want
  end

  test "Advance_Scanners Basic" do
    scanners = %{
      0 => %{depth: 99, scanner: 0, delta: 1},
      1 => %{depth: 2, scanner: 0, delta: 1}
    }

    advanced_once = scanners |> ElixirDay13.advance_scanners()
    advanced_twice = advanced_once |> ElixirDay13.advance_scanners()

    assert advanced_once[0].scanner == 1
    assert advanced_once[1].scanner == 1
    assert advanced_twice[0].scanner == 2
    # Depth = 2, scanner is mod 2, resets to 0
    assert advanced_twice[1].scanner == 0
  end

  test "advance_scanners_n" do
    scanners = %{
      0 => %{depth: 99, scanner: 0, delta: 1},
      1 => %{depth: 2, scanner: 0, delta: 1},
      2 => %{depth: 3, scanner: 0, delta: 1}
    }

    ## 2
    got = scanners |> ElixirDay13.advance_scanners_n(2)
    want = scanners |> ElixirDay13.advance_scanners() |> ElixirDay13.advance_scanners()
    assert got == want

    ## 3
    got = scanners |> ElixirDay13.advance_scanners_n(3)

    want =
      scanners
      |> ElixirDay13.advance_scanners()
      |> ElixirDay13.advance_scanners()
      |> ElixirDay13.advance_scanners()

    assert got == want

    ## 4
    got = scanners |> ElixirDay13.advance_scanners_n(4)

    want =
      scanners
      |> ElixirDay13.advance_scanners()
      |> ElixirDay13.advance_scanners()
      |> ElixirDay13.advance_scanners()
      |> ElixirDay13.advance_scanners()

    assert got == want
  end

  test "Advance_Scanners Reverse Direction" do
    scanners = %{
      0 => %{depth: 3, scanner: 0, delta: 1}
    }

    assert scanners[0].scanner == 0
    scanners = ElixirDay13.advance_scanners(scanners)
    assert scanners[0].scanner == 1
    scanners = ElixirDay13.advance_scanners(scanners)
    assert scanners[0].scanner == 2
    scanners = ElixirDay13.advance_scanners(scanners)
    assert scanners[0].scanner == 1
    scanners = ElixirDay13.advance_scanners(scanners)
    assert scanners[0].scanner == 0
    scanners = ElixirDay13.advance_scanners(scanners)
    assert scanners[0].scanner == 1
    scanners = ElixirDay13.advance_scanners(scanners)
    assert scanners[0].scanner == 2
  end

  test "Part 1 Examples" do
    got =
      Parse.parse_file("../input_small.txt")
      |> ElixirDay13.trip_severity()

    want = 24

    assert got == want
  end

  test "Part 1" do
    got =
      Parse.parse_file("../input.txt")
      |> ElixirDay13.trip_severity()

    want = 2264

    assert got == want
  end

  test "Part 2 Examples" do
    got =
      Parse.parse_file("../input_small.txt")
      |> ElixirDay13.part2_sim()

    want = 10

    assert got == want

    got =
      Parse.parse_file("../input_small.txt")
      |> ElixirDay13.part2_mod()

    want = 10

    assert got == want
  end

  ## Part 2 real. Answer should be 3875838
  ## Currently takes two minutes, too long for an automated test.
end
