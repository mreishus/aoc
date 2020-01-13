defmodule Day07Test do
  alias Elixir2016.Day07
  use ExUnit.Case

  test "part 1" do
    assert Day07.part1("../inputs/07/input.txt") == 110
  end

  test "part 2" do
    assert Day07.part2("../inputs/07/input.txt") == 242
  end

  test "remove_hypernet" do
    assert Day07.remove_hypernet("abba[mnop]qrst") == ["abba", "qrst"]
    assert Day07.remove_hypernet("abba[mnop]qrst[another]z") == ["abba", "qrst", "z"]
    assert Day07.remove_hypernet("abcd[bddb]xyyx") == ["abcd", "xyyx"]
    assert Day07.remove_hypernet("aaaa[qwer]tyui") == ["aaaa", "tyui"]
    assert Day07.remove_hypernet("ioxxoj[asdfgh]zxcvbn") == ["ioxxoj", "zxcvbn"]
  end

  test "tls" do
    assert Day07.tls?("abba[mnop]qrst") == true
    assert Day07.tls?("abcd[bddb]xyyx") == false
    assert Day07.tls?("aaaa[qwer]tyui") == false
    assert Day07.tls?("ioxxoj[asdfgh]zxcvbn") == true
  end

  test "ssl" do
    assert Day07.ssl?("aba[bab]xyz") == true
    assert Day07.ssl?("xyx[xyx]xyx") == false
    assert Day07.ssl?("aaa[kek]eke") == true
    assert Day07.ssl?("zazbz[bzb]cdb") == true
  end
end
