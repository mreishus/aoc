defmodule Day03Test do
  alias Elixir2021.{Day03}
  use ExUnit.Case

  test "part 1" do
    assert Day03.part1("../inputs/03/input_small.txt") == 198
    assert Day03.part1("../inputs/03/input.txt") == 3_882_564
  end

  test "part 2" do
    assert Day03.part2("../inputs/03/input_small.txt") == 230
    assert Day03.part2("../inputs/03/input.txt") == 3_385_170
  end
end
