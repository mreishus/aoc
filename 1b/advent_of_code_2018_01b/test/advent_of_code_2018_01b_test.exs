defmodule AdventOfCode201801bTest do
  use ExUnit.Case
  doctest AdventOfCode201801b

  test "first_repeated_sum works without replaying the list" do
    list = [ +1, +1, +1, +1, +1, +1, +1, +1, +1, -5, +1, +1 ]
    # Should sum up to 9, then remove 5 = 4 is first duplicate
    assert AdventOfCode201801b.first_repeated_sum(list) == 4
  end

  test "first_repeated_sum works with replaying the list" do
    list = [ +10, +10, +10, +1, +1, +1, +1, +1, +10, -30 ]
    assert AdventOfCode201801b.first_repeated_sum(list) == 35
  end

  test "first_repeated_sum works with replaying the list, and counts 0 as seen" do
    list = [ +1, +1, +1, +1, +1, -6]
    assert AdventOfCode201801b.first_repeated_sum(list) == 0
  end
end

