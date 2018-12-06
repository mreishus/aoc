defmodule AdventOfCode201805Test do
  use ExUnit.Case
  doctest AdventOfCode201805

  test "part1_small" do
    assert AdventOfCode201805.part1("input_small.txt") == 10
  end
  test "part1" do
    assert AdventOfCode201805.part1("input.txt") == 10638
  end
end
