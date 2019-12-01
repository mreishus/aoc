defmodule ElixirDay01.BigFlow do
  @moduledoc """
  Use Flow to split up the work into chunks of 500, which run
  in parallel.
  """
  def solve_parallel(filename) do
    ElixirDay01.parse(filename)
    |> Flow.from_enumerable()
    |> Flow.partition()
    |> Flow.map(&ElixirDay01.fuel/1)
    |> Flow.reduce(fn -> [0] end, fn x, [h | _acc] -> [x + h] end)
    |> Enum.sum()
    |> IO.inspect(label: "Part 1")

    ElixirDay01.parse(filename)
    |> Flow.from_enumerable()
    |> Flow.partition()
    |> Flow.map(&ElixirDay01.fuel_total/1)
    |> Flow.reduce(fn -> [0] end, fn x, [h | _acc] -> [x + h] end)
    |> Enum.sum()
    |> IO.inspect(label: "Part 2")
  end

  def main do
    solve_parallel("../input_large.txt")
  end
end
