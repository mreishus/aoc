defmodule Day02Test do
  alias Elixir2021.{Day02}
  use ExUnit.Case

  test "part 1" do
    assert Day02.part1("../inputs/02/input_small.txt") == 150
    assert Day02.part1("../inputs/02/input.txt") == 2_322_630
  end

  test "part 2" do
    assert Day02.part2("../inputs/02/input_small.txt") == 900
    assert Day02.part2("../inputs/02/input.txt") == 2_105_273_490
  end
end
