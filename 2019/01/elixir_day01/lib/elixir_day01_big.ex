defmodule ElixirDay01.Big do
  @moduledoc """
  Manually split up the work into chunks of 5000, which run
  in parallel.  No external dependencies needed.
  """

  def pmap(collection, func) do
    collection
    |> Enum.map(&Task.async(fn -> func.(&1) end))
    |> Enum.map(&Task.await/1)
  end

  def solve_parallel(filename) do
    ElixirDay01.parse(filename)
    |> Stream.chunk_every(5000)
    |> pmap(&solve_p1/1)
    |> Enum.sum()
    |> IO.inspect(label: "Part 1 Chunk")

    ElixirDay01.parse(filename)
    |> Stream.chunk_every(5000)
    |> pmap(&solve_p2/1)
    |> Enum.sum()
    |> IO.inspect(label: "Part 2 Chunk")
  end

  def solve_p1(list) do
    list
    |> Stream.map(&ElixirDay01.fuel/1)
    |> Enum.sum()
  end

  def solve_p2(list) do
    list
    |> Stream.map(&ElixirDay01.fuel_total/1)
    |> Enum.sum()
  end

  def main do
    solve_parallel("../input_large.txt")
  end
end
