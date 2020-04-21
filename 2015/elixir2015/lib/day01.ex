defmodule Elixir2015.Day01 do
  def parse() do
    File.read!("../inputs/01/input.txt")
    |> String.graphemes()
  end

  def part1() do
    parse()
    |> Enum.reduce(0, fn char, count ->
      cond do
        char == "(" ->
          count + 1

        char == ")" ->
          count - 1

        true ->
          raise "Unknown character"
      end
    end)
  end

  def part2() do
    parse()
    |> Enum.with_index(1)
    |> Enum.reduce_while(0, fn {char, floor}, count ->
      new_count =
        cond do
          char == "(" ->
            count + 1

          char == ")" ->
            count - 1

          true ->
            raise "Unknown character"
        end

      if new_count == -1 do
        {:halt, floor}
      else
        {:cont, new_count}
      end
    end)
  end
end
