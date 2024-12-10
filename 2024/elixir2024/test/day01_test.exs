defmodule Day01Test do
  alias Elixir2024.{Day01}
  use ExUnit.Case

  test "part 1" do
    # assert Day01.part1("../inputs/01/input_small.txt") == 11
    assert Day01.part1("../inputs/01/input.txt") == 2_164_381
  end

  test "part 2" do
    # assert Day01.part2("../inputs/01/input_small.txt") == 31
    assert Day01.part2("../inputs/01/input.txt") == 20_719_933
  end
end
