defmodule Elixir2020.Day06Test do
  use ExUnit.Case
  import Elixir2020.Day06

  test "part1" do
    assert part1("../inputs/06/input.txt") == 6799
  end

  test "part2" do
    assert part2("../inputs/06/input.txt") == 3354
  end
end
