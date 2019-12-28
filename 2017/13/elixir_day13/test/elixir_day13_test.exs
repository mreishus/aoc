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
end
