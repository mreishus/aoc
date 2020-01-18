defmodule Parallel do
  def pmap(collection, func) do
    collection
    |> Enum.map(&Task.async(fn -> func.(&1) end))
    |> Enum.map(&Task.await/1)
  end

  def pmap2(collection, func, arg2) do
    collection
    |> Enum.map(&Task.async(fn -> func.(&1, arg2) end))
    |> Enum.map(&Task.await/1)
  end
end
