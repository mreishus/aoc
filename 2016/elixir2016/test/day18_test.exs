defmodule Day18Test do
  alias Elixir2016.Day18
  use ExUnit.Case

  test "part 1 examples" do
    got =
      ".^^.^.^^^^"
      |> String.graphemes()
      |> Day18.part1_count(10)

    want = 38
    assert got == want
  end
end
