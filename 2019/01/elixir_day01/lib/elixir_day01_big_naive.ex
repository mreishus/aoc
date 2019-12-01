defmodule ElixirDay01.BigNaive do
  @moduledoc """
  Naive implementation of parallelism.  Since input_large.txt is 
  one million lines long, this actually starts a million processes at once!
  It's actually slower than running it linerally, but hey, I wanted to run
  a million processes.
  """
  def pmap(collection, func) do
    collection
    |> Enum.map(&Task.async(fn -> func.(&1) end))
    |> Enum.map(&Task.await/1)
  end

  def solve_parallel(filename) do
    ElixirDay01.parse(filename)
    |> pmap(&ElixirDay01.fuel/1)
    |> Enum.sum()
    |> IO.inspect(label: "Part 1")

    ElixirDay01.parse(filename)
    |> pmap(&ElixirDay01.fuel_total/1)
    |> Enum.sum()
    |> IO.inspect(label: "Part 2")
  end

  def main do
    solve_parallel("../input_large.txt")
  end
end
