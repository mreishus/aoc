defmodule AdventOfCode201802Test.Part1 do
  use ExUnit.Case
  doctest AdventOfCode201802.Part1

  test "get_char_counts" do
    str = "hello"
    expected_char_counts = %{"h" => 1, "e" => 1, "l" => 2, "o" => 1}
    assert AdventOfCode201802.Part1.get_char_counts(str) == expected_char_counts
  end

  test "string_has_char_repeated_x_times" do
    assert AdventOfCode201802.Part1.string_has_char_repeated_x_times("hello", 2) == true
    assert AdventOfCode201802.Part1.string_has_char_repeated_x_times("hello", 3) == false
  end

  test "compute_checksum" do
    list = ["hello", "goodbye", "threee", "threee_2", "threee_3"]
    assert AdventOfCode201802.Part1.compute_checksum(list) == 6
  end
end

defmodule AdventOfCode201802Test.Part2 do
  use ExUnit.Case
  doctest AdventOfCode201802.Part2

  test "is_one_char_off" do
    assert AdventOfCode201802.Part2.are_strings_one_char_off("hello", "hello") == false
    assert AdventOfCode201802.Part2.are_strings_one_char_off("hellX", "hello") == true
    assert AdventOfCode201802.Part2.are_strings_one_char_off("hello", "hellX") == true
    assert AdventOfCode201802.Part2.are_strings_one_char_off("hello", "helloi") == false
  end

  test "get_strings_no_diff" do
    assert AdventOfCode201802.Part2.get_strings_no_diff("ZZhelloYYend", "AAhelloBBend") == "helloend"
  end

end
