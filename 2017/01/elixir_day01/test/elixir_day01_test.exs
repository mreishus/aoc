defmodule ElixirDay01Test do
  use ExUnit.Case
  doctest ElixirDay01

  test "Rotate String" do
    assert ElixirDay01.rotate_string("abcd", 1) == "bcda"
    assert ElixirDay01.rotate_string("abcd", 2) == "cdab"
  end

  test "Part 1" do
    [["1122", 3], ["1111", 4], ["1234", 0], ["91212129", 9]]
    |> Enum.each(fn [string, want] ->
      assert ElixirDay01.part1(string) == want
    end)
  end

  test "Part 2" do
    [
      ["1212", 6],
      ["1221", 0],
      ["123425", 4],
      ["123123", 12],
      ["12131415", 4]
    ]
    |> Enum.each(fn [string, want] ->
      assert ElixirDay01.part2(string) == want
    end)
  end
end
