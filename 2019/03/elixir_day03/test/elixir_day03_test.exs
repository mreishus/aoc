defmodule ElixirDay03Test do
  use ExUnit.Case
  doctest ElixirDay03

  test "greets the world" do
    assert ElixirDay03.hello() == :world
  end
end
