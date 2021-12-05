defmodule Day01Test do
  alias Elixir2021.{Day01}
  use ExUnit.Case

  test "part 1" do
    assert Day01.part1("../inputs/01/input_small.txt") == 7
    assert Day01.part1("../inputs/01/input.txt") == 1298
  end

  test "part 2" do
    assert Day01.part2("../inputs/01/input_small.txt") == 5
    assert Day01.part2("../inputs/01/input.txt") == 1248
  end
end
