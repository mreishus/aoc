defmodule AdventOfCode201805Test do
  use ExUnit.Case
  doctest AdventOfCode201805

  test "part1_small" do
    assert AdventOfCode201805.part1("input_small.txt") == 10
  end
  test "part1" do
    assert AdventOfCode201805.part1("input.txt") == 10638
  end
  test "part2_small" do
    assert AdventOfCode201805.part2("input_small.txt") == 4
  end
  test "part2" do
    assert AdventOfCode201805.part2("input.txt") == 4944
  end
end
