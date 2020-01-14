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

  test "expand2" do
    assert Day09.expand2("(3x3)XYZ") == String.length("XYZXYZXYZ")
    assert Day09.expand2("X(8x2)(3x3)ABCY") == String.length("XABCABCABCABCABCABCY")
    assert Day09.expand2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445
    assert Day09.expand2("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241_920
  end
end
