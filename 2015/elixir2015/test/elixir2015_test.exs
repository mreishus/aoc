defmodule Elixir2015Test do
  use ExUnit.Case
  doctest Elixir2015

  test "greets the world" do
    assert Elixir2015.hello() == :world
  end
end
