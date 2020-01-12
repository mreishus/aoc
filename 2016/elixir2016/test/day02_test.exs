defmodule Day02Test do
  alias Elixir2016.{Day02}
  use ExUnit.Case

  test "part 1" do
    assert Day02.part1("../inputs/02/input_small.txt") == "1985"
    assert Day02.part1("../inputs/02/input.txt") == "14894"
  end

  test "part 2" do
    assert Day02.part2("../inputs/02/input_small.txt") == "5DB3"
  end
end
