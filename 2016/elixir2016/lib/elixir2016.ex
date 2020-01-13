defmodule Elixir2016 do
  alias Elixir2016.{Day02, Day03, Day04}

  @moduledoc """
  Documentation for Elixir2016.
  """
  def main do
    ## Day 2
    Day02.part1("../inputs/02/input.txt")
    |> IO.inspect(label: "2016 Day 02 Part 1")

    Day02.part2("../inputs/02/input.txt")
    |> IO.inspect(label: "2016 Day 02 Part 2")

    ## Day 3
    Day03.part1("../inputs/03/input.txt")
    |> IO.inspect(label: "2016 Day 03 Part 1")

    Day03.part2("../inputs/03/input.txt")
    |> IO.inspect(label: "2016 Day 03 Part 2")

    ## Day 4
    Day04.part1("../inputs/04/input.txt")
    |> IO.inspect(label: "2016 Day 04 Part 1")

    Day04.part2("../inputs/04/input.txt")
    |> IO.inspect(label: "2016 Day 04 Part 2")
  end
end
