defmodule Elixir2020.Day02 do
  def parse(filename) do
    File.stream!(filename)
    |> Enum.map(&String.trim/1)
    |> Enum.map(&parse_rules/1)
  end

  def parse_rules(string) do
    [_, lower, upper, letter, password] = Regex.run(~r/^(\d+)-(\d+) (\w+): (\w+)$/, string)

    %{
      lower: String.to_integer(lower),
      upper: String.to_integer(upper),
      letter: letter,
      password: password
    }
  end

  def test1(%{lower: lower, upper: upper, letter: letter, password: password}) do
    count =
      password
      |> String.graphemes()
      |> Enum.filter(fn x -> x == letter end)
      |> Enum.count()

    lower <= count and count <= upper
  end

  def test2(%{lower: lower, upper: upper, letter: letter, password: password}) do
    lower_match = String.at(password, lower - 1) == letter
    upper_match = String.at(password, upper - 1) == letter
    lower_match != upper_match
  end

  def part1(filename) do
    filename
    |> parse()
    |> Enum.filter(&test1/1)
    |> Enum.count()
  end

  def part2(filename) do
    filename
    |> parse()
    |> Enum.filter(&test2/1)
    |> Enum.count()
  end
end
