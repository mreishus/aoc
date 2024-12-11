defmodule Day04Test do
  alias Elixir2024.{Day04}
  use ExUnit.Case

  test "part 1" do
    assert Day04.part1("../inputs/04/input_small.txt") == 18
    assert Day04.part1("../inputs/04/input.txt") == 2583
  end

  test "part 2" do
    assert Day04.part2("../inputs/04/input_small.txt") == 9
    assert Day04.part2("../inputs/04/input.txt") == 1978
  end
end
