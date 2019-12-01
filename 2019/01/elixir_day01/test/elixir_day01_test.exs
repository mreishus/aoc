defmodule ElixirDay01Test do
  use ExUnit.Case
  doctest ElixirDay01

  test "greets the world" do
    assert ElixirDay01.hello() == :world
  end
end
