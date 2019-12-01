defmodule ElixirDay01 do
  def fuel(num), do: (floor(num / 3) - 2) |> max(0)

  def fuel_total(num), do: fuel_total(num, 0)

  def fuel_total(num, acc) do
    fuel = fuel(num)
    if fuel > 0, do: fuel_total(fuel, acc + fuel), else: acc
  end

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.to_integer/1)
  end

  def main do
    parse("../input.txt")
    |> Stream.map(&fuel/1)
    |> Enum.sum()
    |> IO.inspect(label: "Part 1")

    parse("../input.txt")
    |> Stream.map(&fuel_total/1)
    |> Enum.sum()
    |> IO.inspect(label: "Part 2")
  end
end
