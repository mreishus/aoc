defmodule Day07Test do
  alias Elixir2016.Day07
  use ExUnit.Case

  # test "part 1" do
  #   assert Day07.part1("../inputs/07/input_small.txt") == "easter"
  #   assert Day07.part1("../inputs/07/input.txt") == "ursvoerv"
  # end

  # test "part 2" do
  #   assert Day07.part2("../inputs/07/input_small.txt") == "advent"
  #   assert Day07.part2("../inputs/07/input.txt") == "vomaypnn"
  # end

  test "remove_hypernet" do
    assert Day07.remove_hypernet("abba[mnop]qrst") == "abbaqrst"
    assert Day07.remove_hypernet("abba[mnop]qrst[another]z") == "abbaqrstz"
    assert Day07.remove_hypernet("abcd[bddb]xyyx") == "abcdxyyx"
    assert Day07.remove_hypernet("aaaa[qwer]tyui") == "aaaatyui"
    assert Day07.remove_hypernet("ioxxoj[asdfgh]zxcvbn") == "ioxxojzxcvbn"
  end

  test "tls" do
    assert Day07.tls?("abba[mnop]qrst") == true
    assert Day07.tls?("abcd[bddb]xyyx") == false
    assert Day07.tls?("aaaa[qwer]tyui") == false
    assert Day07.tls?("ioxxoj[asdfgh]zxcvbn") == true
  end
end
