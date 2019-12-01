defmodule ElixirDay01Test do
  use ExUnit.Case
  doctest ElixirDay01
  import ElixirDay01, only: :functions

  test "fuel" do
    assert fuel(12) == 2
    assert fuel(14) == 2
    assert fuel(1_969) == 654
    assert fuel(100_756) == 33_583
  end

  test "fuel_total" do
    assert fuel_total(14) == 2
    assert fuel_total(1_969) == 966
    assert fuel_total(100_756) == 50_346
  end
end
