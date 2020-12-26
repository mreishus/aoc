defmodule Elixir2020.Day04 do
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
    |> String.split("\n\n")
    |> Enum.map(&parse_passport/1)
  end

  def parse_passport(pp) do
    pp
    |> String.split(~r/\s+/)
    |> Enum.map(fn chunk ->
      [left, right] = String.split(chunk, ":")
      {left, right}
    end)
    |> Map.new()
  end

  def required(), do: ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"] |> MapSet.new()

  def has_required_fields(pp) do
    has_keys = pp |> Map.keys() |> MapSet.new()
    0 == MapSet.difference(required(), has_keys) |> Enum.count()
  end

  def valid?(pp) do
    pp
    |> Enum.all?(fn {k, v} ->
      valid_field?(k, v)
    end)
  end

  def valid_field?("byr", val), do: string_is_number_between(val, 1920, 2002)
  def valid_field?("iyr", val), do: string_is_number_between(val, 2010, 2020)
  def valid_field?("eyr", val), do: string_is_number_between(val, 2020, 2030)

  def valid_field?("hgt", val) do
    case Regex.run(~r/^(\d+)(cm|in)$/, val) do
      [_, num, "cm"] ->
        num = String.to_integer(num)
        150 <= num and num <= 193

      [_, num, "in"] ->
        num = String.to_integer(num)
        59 <= num and num <= 76

      _ ->
        false
    end
  end

  def valid_field?("hcl", val), do: String.match?(val, ~r/^#[a-f0-9]{6}$/)
  def valid_field?("ecl", val), do: String.match?(val, ~r/^(amb|blu|brn|gry|grn|hzl|oth)$/)
  def valid_field?("pid", val), do: String.match?(val, ~r/^\d{9}$/)
  def valid_field?("cid", _), do: true

  def string_is_number_between(val, low, high) do
    case Integer.parse(val) do
      {x, ""} -> low <= x and x <= high
      _ -> false
    end
  end

  def part1(filename) do
    filename
    |> parse()
    |> Enum.filter(&has_required_fields/1)
    |> Enum.count()
  end

  def part2(filename) do
    filename
    |> parse()
    |> Enum.filter(&has_required_fields/1)
    |> Enum.filter(&valid?/1)
    |> Enum.count()
  end
end
