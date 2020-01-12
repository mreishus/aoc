defmodule Elixir2016 do
  alias Elixir2016.{Day02, Day03}

  @moduledoc """
  Documentation for Elixir2016.
  """
  def main do
    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2016 Day 02 Part 1")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2016 Day 02 Part 2")

    Day03.part1("../inputs/03/input.txt")
    |> IO.inspect(label: "2016 Day 03 Part 1")

    Day03.part2("../inputs/03/input.txt")
    |> IO.inspect(label: "2016 Day 03 Part 2")
  end
end
