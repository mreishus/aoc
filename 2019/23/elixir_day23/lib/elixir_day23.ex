defmodule ElixirDay23 do
  @moduledoc """
  Documentation for ElixirDay23.
  """
  alias ElixirDay23.{Coordinator}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  @doc """
  First 255 packet: 30757, 22134
  """
  def main do
    program = parse("../../23/input.txt")
    how_many = 50

    {:ok, pid} = Coordinator.start(program, how_many, self())

    pid
    |> IO.inspect(label: "coordinator pid")

    receive do
      {:answers, p1, p2} ->
        p1 |> IO.inspect(label: "Part 1")
        p2 |> IO.inspect(label: "Part 2")
    end
  end
end
