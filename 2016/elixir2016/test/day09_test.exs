defmodule Day09Test do
  alias Elixir2016.Day09
  use ExUnit.Case

  test "part 1" do
    assert Day09.part1("../inputs/09/input.txt") == 152_851
  end

  test "expand" do
    assert Day09.expand("ADVENT") == "ADVENT"
    assert Day09.expand("A(1x5)BC") == "ABBBBBC"
    assert Day09.expand("(3x3)XYZ") == "XYZXYZXYZ"
    assert Day09.expand("A(2x2)BCD(2x2)EFG") == "ABCBCDEFEFG"
    assert Day09.expand("(6x1)(1x3)A") == "(1x3)A"
    assert Day09.expand("X(8x2)(3x3)ABCY") == "X(3x3)ABC(3x3)ABCY"
  end
end
