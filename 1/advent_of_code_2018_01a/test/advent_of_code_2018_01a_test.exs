defmodule AdventOfCode201801aTest do
  use ExUnit.Case
  doctest AdventOfCode201801a

  test "sums numbers" do
    assert AdventOfCode201801a.sum([1, 2, 3, 4, 5]) == 15
  end
end
