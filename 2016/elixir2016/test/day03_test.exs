defmodule Day03Test do
  alias Elixir2016.{Day03}
  use ExUnit.Case

  test "part 1" do
    assert Day03.part1("../inputs/03/input.txt") == 1050
  end

  test "part 2" do
    assert Day03.part2("../inputs/03/input.txt") == 1921
  end

  test "triangle?" do
    assert Day03.triangle?([5, 10, 25]) == false
    assert Day03.triangle?([5, 10, 11]) == true
  end
end
