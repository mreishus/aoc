defmodule Elixir2021.Day06 do
  def parse(filename) do
    File.stream!(filename)
    |> Enum.map(&String.trim/1)
    |> Enum.at(0)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def step(a, count) do
    m =
      Matrex.new([
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0]
      ])

    m =
      1..(count - 1)
      |> Enum.reduce(m, fn _x, acc ->
        Matrex.dot(m, acc)
      end)

    Matrex.dot(m, a)
  end

  def part1(filename) do
    # "3,4,3,1,2"                        input
    # [3, 4, 3, 1, 2]                    parsed
    # %{1 => 1, 2 => 1, 3 => 2, 4 => 1}  freqs
    # [0, 1, 1, 2, 1, 0, 0, 0, 0]        a

    freqs =
      parse(filename)
      |> Enum.frequencies()

    a =
      0..8
      |> Enum.map(fn x ->
        Map.get(freqs, x, 0)
      end)

    Matrex.new([a])
    |> Matrex.transpose()
    |> step(80)
    |> Enum.sum()
  end

  def part2(filename) do
    freqs =
      parse(filename)
      |> Enum.frequencies()

    a =
      0..8
      |> Enum.map(fn x ->
        Map.get(freqs, x, 0)
      end)

    Matrex.new([a])
    |> Matrex.transpose()
    |> step(256)
    |> Enum.sum()
  end
end
