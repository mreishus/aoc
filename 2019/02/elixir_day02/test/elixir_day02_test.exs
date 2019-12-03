defmodule ElixirDay02Test do
  use ExUnit.Case
  doctest ElixirDay02

  test "greets the world" do
    assert ElixirDay02.hello() == :world
  end
end
