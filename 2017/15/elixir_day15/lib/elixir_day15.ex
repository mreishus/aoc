defmodule ElixirDay15 do
  @moduledoc """
  Documentation for ElixirDay15.
  """
  use Bitwise

  @right_16 65535

  ### Functoins for part 1

  def genA(input), do: rem(input * 16807, 2_147_483_647)

  def genB(input), do: rem(input * 48271, 2_147_483_647)

  def compare(startA, startB, count), do: do_compare(startA, startB, count, 0)

  def do_compare(_startA, _startB, 0, score), do: score

  def do_compare(startA, startB, count, score) do
    a = genA(startA)
    b = genB(startB)

    if (a &&& @right_16) == (b &&& @right_16) do
      do_compare(a, b, count - 1, score + 1)
    else
      do_compare(a, b, count - 1, score)
    end
  end

  ### All "2" functions are for part 2

  def genA2(input) do
    a = genA(input)
    if rem(a, 4) == 0, do: a, else: genA2(a)
  end

  def genB2(input) do
    b = genB(input)
    if rem(b, 8) == 0, do: b, else: genB2(b)
  end

  def compare2(startA, startB, count), do: do_compare2(startA, startB, count, 0)

  def do_compare2(_startA, _startB, 0, score), do: score

  def do_compare2(startA, startB, count, score) do
    a = genA2(startA)
    b = genB2(startB)

    if (a &&& @right_16) == (b &&& @right_16) do
      do_compare2(a, b, count - 1, score + 1)
    else
      do_compare2(a, b, count - 1, score)
    end
  end

  ### Driver

  def main do
    compare(289, 629, 40_000_000)
    |> IO.inspect(label: "Part 1")

    compare2(289, 629, 5_000_000)
    |> IO.inspect(label: "Part 2")
  end
end
