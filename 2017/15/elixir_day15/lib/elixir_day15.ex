defmodule ElixirDay15 do
  @moduledoc """
  Documentation for ElixirDay15.
  """
  use Bitwise

  @right_16 65535

  def genA(input) do
    rem(input * 16807, 2_147_483_647)
  end

  def genB(input) do
    rem(input * 48271, 2_147_483_647)
  end

  def compare(startA, startB, count) do
    do_compare(startA, startB, count, 0)
  end

  def do_compare(_startA, _startB, 0, score) do
    score
  end

  def do_compare(startA, startB, count, score) do
    a = genA(startA)
    b = genB(startB)

    if (a &&& @right_16) == (b &&& @right_16) do
      do_compare(a, b, count - 1, score + 1)
    else
      do_compare(a, b, count - 1, score)
    end
  end

  def main do
    # assert compare(65, 8921, 3) == 3
    # compare(65, 8921, 40_000_000) == 588
    compare(289, 629, 40_000_000)
    |> IO.inspect(label: "Part 1")
  end
end
