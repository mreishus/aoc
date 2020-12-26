defmodule Elixir2020.Day07Test do
  use ExUnit.Case
  import Elixir2020.Day07

  test "part1" do
    assert part1("../inputs/07/input.txt") == 211
  end

  test "part2" do
    assert part2("../inputs/07/input.txt") == 12414
  end
end
