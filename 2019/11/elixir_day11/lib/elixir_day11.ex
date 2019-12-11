defmodule ElixirDay11 do
  @moduledoc """
  Documentation for ElixirDay11.
  """
  alias ElixirDay11.{PainterRobot}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def main do
    parse("../../11/input.txt")
    |> PainterRobot.new(0)
    |> PainterRobot.execute()
    |> PainterRobot.count_painted_squares()
    |> IO.inspect(label: "day 11 part 1")

    parse("../../11/input.txt")
    |> PainterRobot.new(1)
    |> PainterRobot.execute()
    |> PainterRobot.display()
    |> IO.puts()
  end
end
