defmodule Elixir2015.Day02 do
  def parse() do
    File.read!("../inputs/02/input.txt")
    |> String.split("\n")
    |> Enum.map(&parse_item/1)
    |> Enum.reject(fn item -> item == nil end)
  end

  def parse_item(""), do: nil

  def parse_item(item) do
    [l, w, h] =
      item
      |> String.split("x")
      |> Enum.map(&String.to_integer/1)

    %{l: l, w: w, h: h}
  end

  def add_surface_slack(%{l: l, w: w, h: h} = item) do
    surface = 2 * l * w + 2 * w * h + 2 * h * l
    slack = smallest_side(item)

    item
    |> Map.put(:surface, surface)
    |> Map.put(:slack, slack)
  end

  def smallest_side(%{l: l, w: w, h: h}) do
    [l * w, w * h, h * l]
    |> Enum.sort()
    |> Enum.at(0)
  end

  def add_ribbon_bow(%{l: l, w: w, h: h} = item) do
    sides = [l, w, h] |> Enum.sort()
    ribbon = 2 * Enum.at(sides, 0) + 2 * Enum.at(sides, 1)
    bow = l * w * h

    item
    |> Map.put(:ribbon, ribbon)
    |> Map.put(:bow, bow)
  end

  def part1() do
    parse()
    |> Enum.map(&add_surface_slack/1)
    |> Enum.reduce(0, fn %{surface: surface, slack: slack}, acc ->
      acc + surface + slack
    end)
  end

  def part2() do
    parse()
    |> Enum.map(&add_ribbon_bow/1)
    |> Enum.reduce(0, fn %{ribbon: ribbon, bow: bow}, acc ->
      acc + ribbon + bow
    end)
  end
end
