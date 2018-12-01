defmodule AdventOfCode201801aTest do
  use ExUnit.Case
  doctest AdventOfCode201801a

  test "adds positive numbers" do
    assert AdventOfCode201801a.sum_strings_with_operator("+10", 100) == 110
  end

  test "subtracts negative numbers" do
    assert AdventOfCode201801a.sum_strings_with_operator("-10", 100) == 90
  end

  test "0 keeps sum" do
    assert AdventOfCode201801a.sum_strings_with_operator("+0", 100) == 100
    assert AdventOfCode201801a.sum_strings_with_operator("-0", 100) == 100
  end
end
