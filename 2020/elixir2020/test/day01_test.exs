defmodule Elixir2020.Day01Test do
  use ExUnit.Case
  import Elixir2020.Day01

  test "part1" do
    assert part1("../inputs/01/input.txt") == 121_396
  end

  test "part2" do
    assert part2("../inputs/01/input.txt") == 73_616_634
  end
end
