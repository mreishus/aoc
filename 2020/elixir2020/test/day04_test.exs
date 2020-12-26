defmodule Elixir2020.Day04Test do
  use ExUnit.Case
  import Elixir2020.Day04

  test "part1" do
    assert part1("../inputs/04/input.txt") == 213
  end

  test "part2" do
    assert part2("../inputs/04/input.txt") == 147
  end
end
