defmodule Elixir2020.Day02Test do
  use ExUnit.Case
  import Elixir2020.Day02

  test "part1" do
    assert part1("../inputs/02/input.txt") == 628
  end

  test "part2" do
    assert part2("../inputs/02/input.txt") == 705
  end
end
