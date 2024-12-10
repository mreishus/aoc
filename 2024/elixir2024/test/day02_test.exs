defmodule Day02Test do
  alias Elixir2024.{Day02}
  use ExUnit.Case

  test "part 1" do
    assert Day02.part1("../inputs/02/input_small.txt") == 2
    assert Day02.part1("../inputs/02/input.txt") == 680
  end

  test "part 2" do
    assert Day02.part2("../inputs/02/input_small.txt") == 4
    assert Day02.part2("../inputs/02/input.txt") == 710
  end
end
