defmodule Elixir2024.Day03 do
  def parse(filename) do
    {:ok, file} = File.read(filename)
    file
  end

  defp sum_multiplications(str) do
    Regex.scan(~r/mul\((\d+),(\d+)\)/, str)
    |> Enum.map(fn [_string, a, b] -> String.to_integer(a) * String.to_integer(b) end)
    |> Enum.sum()
  end

  def part1(filename), do: filename |> parse() |> sum_multiplications()
  
  def part2(filename) do
    filename
    |> parse()
    |> then(&Regex.replace(~r/don't\(\).*?(do\(\)|\z)/ms, &1, ""))
    |> sum_multiplications()
  end
end
