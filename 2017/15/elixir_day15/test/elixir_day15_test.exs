defmodule ElixirDay15Test do
  use ExUnit.Case
  doctest ElixirDay15

  test "Examples from problem" do
    assert ElixirDay15.compare(65, 8921, 3) == 1
    assert ElixirDay15.compare(65, 8921, 40_000_000) == 588
    assert ElixirDay15.compare2(65, 8921, 1055) == 0
    assert ElixirDay15.compare2(65, 8921, 1056) == 1
  end

  test "Actual problem" do
    assert ElixirDay15.compare(289, 629, 40_000_000) == 638
    assert ElixirDay15.compare2(289, 629, 5_000_000) == 343
  end
end
