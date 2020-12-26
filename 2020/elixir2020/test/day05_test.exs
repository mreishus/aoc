defmodule Elixir2020.Day05Test do
  use ExUnit.Case
  import Elixir2020.Day05

  test "part1" do
    assert part1("../inputs/05/input.txt") == 822
  end

  test "part2" do
    assert part2("../inputs/05/input.txt") == 705
  end
end
