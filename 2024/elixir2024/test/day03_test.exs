defmodule Day03Test do
  alias Elixir2024.{Day03}
  use ExUnit.Case

  test "part 1" do
    assert Day03.part1("../inputs/03/input_small.txt") == 161
    assert Day03.part1("../inputs/03/input.txt") == 196_826_776
  end

  test "part 2" do
    assert Day03.part2("../inputs/03/input_small2.txt") == 48
    assert Day03.part2("../inputs/03/input.txt") == 106_780_429
  end
end
