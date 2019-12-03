defmodule ElixirDay02 do
  @moduledoc """
  Documentation for ElixirDay02.
  """

  @doc """
  Hello world.

  ## Examples

      iex> ElixirDay02.hello()
      :world

  """
  def hello do
    :world
  end

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
    |> Array.from_list()
  end

  def part1(program) do
    program
    |> Array.set(1, 12)
    |> Array.set(2, 2)
    |> compute()
    |> Array.get(0)
  end

  def part2_compute(program, x, y) do
    program
    |> Array.set(1, x)
    |> Array.set(2, y)
    |> compute()
    |> Array.get(0)
  end

  def part2(program) do
    range = 0..100

    range
    |> Enum.reduce_while(0, fn x, acc ->
      inner =
        range
        |> Enum.reduce_while(0, fn y, innerAcc ->
          if part2_satisfy?(program, x, y) do
            {:halt, part2_answer(x, y)}
          else
            {:cont, 0}
          end
        end)

      if inner == 0 do
        {:cont, 0}
      else
        {:halt, inner}
      end
    end)
  end

  def part2_satisfy?(program, x, y) do
    part2_compute(program, x, y) == 19_690_720
  end

  def part2_answer(x, y) do
    100 * x + y
  end

  def compute(program) do
    do_compute(program, 0)
  end

  def do_compute(program, i) do
    instruction = Array.get(program, i)
    apply_compute(program, i, instruction)
  end

  # 1 = Add
  def apply_compute(program, i, 1) do
    pos_in1 = Array.get(program, i + 1)
    pos_in2 = Array.get(program, i + 2)
    pos_out = Array.get(program, i + 3)
    result = Array.get(program, pos_in1) + Array.get(program, pos_in2)

    new_program = Array.set(program, pos_out, result)
    do_compute(new_program, i + 4)
  end

  # 2 = Mult
  def apply_compute(program, i, 2) do
    pos_in1 = Array.get(program, i + 1)
    pos_in2 = Array.get(program, i + 2)
    pos_out = Array.get(program, i + 3)
    result = Array.get(program, pos_in1) * Array.get(program, pos_in2)

    new_program = Array.set(program, pos_out, result)
    do_compute(new_program, i + 4)
  end

  # 99 = Stop
  def apply_compute(program, _i, 99) do
    program
  end

  def apply_compute(_program, _i, opcode) do
    raise "Unknown opcode " <> Integer.to_string(opcode)
  end

  def main do
    parse("../input.txt")
    |> part1()
    |> IO.inspect(label: "Part 1")

    parse("../input.txt")
    |> part2()
    |> IO.inspect(label: "Part 2")
  end
end
