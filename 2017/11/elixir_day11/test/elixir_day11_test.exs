defmodule ElixirDay11Test do
  use ExUnit.Case
  doctest ElixirDay11

  test "ElixirDay11.part1 examples" do
    got = ["ne", "ne", "ne"] |> ElixirDay11.part1()
    want = 3
    assert got == want

    got = ["ne", "ne", "sw", "sw"] |> ElixirDay11.part1()
    want = 0
    assert got == want

    got = ["ne", "ne", "s", "s"] |> ElixirDay11.part1()
    want = 2
    assert got == want

    got = ["se", "sw", "se", "sw", "sw"] |> ElixirDay11.part1()
    want = 3
    assert got == want
  end

  test "Part 1 problem" do
    got = ElixirDay11.parse("../input.txt") |> ElixirDay11.part1()
    want = 818
    assert got == want
  end

  test "Part 2 problem" do
    got = ElixirDay11.parse("../input.txt") |> ElixirDay11.part2()
    want = 1596
    assert got == want
  end
end
