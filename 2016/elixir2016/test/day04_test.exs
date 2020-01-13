defmodule Day04Test do
  alias Elixir2016.Day04
  alias Elixir2016.Day04.Rotate
  use ExUnit.Case

  test "part 1" do
    assert Day04.part1("../inputs/04/input.txt") == 278_221
  end

  test "part 2" do
    assert Day04.part2("../inputs/04/input.txt") == 267
  end

  test "valid_room?" do
    assert Day04.valid_room?("aaaaa-bbb-z-y-x-123[abxyz]") == true
    assert Day04.valid_room?("a-b-c-d-e-f-g-h-987[abcde]") == true
    assert Day04.valid_room?("not-a-real-room-404[oarel]") == true
    assert Day04.valid_room?("totally-real-room-200[decoy]") == false
  end

  test "parse_room" do
    want = %{checksum: "decoy", name: "totally-real-room", sector_id: 200}
    assert Day04.parse_room("totally-real-room-200[decoy]") == want
  end

  test "rotate" do
    assert Rotate.rotate("the futurez", 13) == "gur shgherm"
    start = "oiwrjoikxzlkmznu"
    assert start |> Rotate.rotate(13) |> Rotate.rotate(13) == start
    assert Rotate.rotate("qzmt-zixmtkozy-ivhz", 343) == "very-encrypted-name"
  end
end
