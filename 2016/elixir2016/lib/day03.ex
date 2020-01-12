defmodule Elixir2016.Day03 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.split/1)
    |> Stream.map(fn line -> Enum.map(line, &String.to_integer/1) end)
  end

  def part1(filename) do
    parse(filename)
    |> Stream.filter(&triangle?/1)
    |> Enum.count()
  end

  def part2(filename) do
    parse(filename)
    |> Stream.chunk_every(3)
    |> Stream.flat_map(&rotate_three/1)
    |> Stream.filter(&triangle?/1)
    |> Enum.count()
  end

  def triangle?([a, b, c]) do
    a < b + c and b < a + c and c < a + b
  end

  # Is there a better way to do this?
  def rotate_three([[a, b, c], [d, e, f], [g, h, i]]) do
    [
      [a, d, g],
      [b, e, h],
      [c, f, i]
    ]
  end

  def rotate_three(_), do: []
end
