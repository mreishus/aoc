defmodule Day12Test do
  alias Elixir2021.{Day12}
  use ExUnit.Case

  test "part 1" do
    assert Day12.part1("../inputs/12/input_small.txt") == 10
    assert Day12.part1("../inputs/12/input_small2.txt") == 19
    assert Day12.part1("../inputs/12/input_small3.txt") == 226
    assert Day12.part1("../inputs/12/input.txt") == 4754
  end

  test "part 2" do
    assert Day12.part2("../inputs/12/input_small.txt") == 36
    assert Day12.part2("../inputs/12/input_small2.txt") == 103
    assert Day12.part2("../inputs/12/input_small3.txt") == 3509
    assert Day12.part2("../inputs/12/input.txt") == 143_562
  end
end
