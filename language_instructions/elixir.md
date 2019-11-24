# Elixir

## Basic Setup

```fish
set PROJNAME elixir_day01
mix new $PROJNAME
cd $PROJNAME
nvim lib/{$PROJNAME}.ex test/{$PROJNAME}_test.exs Makefile -p
```

## `lib/elixir_day01.ex`

```elixir
defmodule ElixirDay01 do
  @moduledoc """
  Documentation for ElixirDay01.
  """

  def main do
    "This is the main" |> IO.inspect()
  end

  @doc """
  Hello world.

  ## Examples

      iex> ElixirDay01.hello()
      :world

  """
  def hello do
    :world
  end
end
```

## `test/elixir_day01_test.exs`

```elixir
defmodule ElixirDay01Test do
  use ExUnit.Case
  doctest ElixirDay01

  test "greets the world" do
    assert ElixirDay01.hello() == :world
  end
end
```

## `./Makefile` (requires tabs!)

```makefile
run:
        mix run -e "ElixirDay01.main()"
test:
        mix test
repl:
        iex
format:
        mix format
```
