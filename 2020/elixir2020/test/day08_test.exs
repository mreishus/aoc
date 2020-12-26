defmodule Elixir2020.Day08Test do
  use ExUnit.Case
  import Elixir2020.Day08

  test "part1" do
    assert part1("../inputs/08/input.txt") == {:infinite_loop, 1179}
  end

  test "part2" do
    assert part2("../inputs/08/input.txt") == 1089
  end
end
