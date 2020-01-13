defmodule Day06Test do
  alias Elixir2016.Day06
  use ExUnit.Case

  test "part 1" do
    assert Day06.part1("../inputs/06/input_small.txt") == "easter"
    assert Day06.part1("../inputs/06/input.txt") == "ursvoerv"
  end

  test "part 2" do
    assert Day06.part2("../inputs/06/input_small.txt") == "advent"
    assert Day06.part2("../inputs/06/input.txt") == "vomaypnn"
  end
end
