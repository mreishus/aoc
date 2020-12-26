defmodule Elixir2020.Day03Test do
  use ExUnit.Case
  import Elixir2020.Day03

  test "part1" do
    assert part1("../inputs/03/input.txt") == 216
  end

  test "part2" do
    assert part2("../inputs/03/input.txt") == 6_708_199_680
  end
end
