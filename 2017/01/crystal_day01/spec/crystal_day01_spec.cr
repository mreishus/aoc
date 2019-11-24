require "./spec_helper"

describe CrystalDay01 do
  # TODO: Write tests

  it "works computing part1" do
    #cases : Array(Tuple(String, Int32))
    cases = [{"1122", 3}, {"1111", 4}, {"1234", 0}, {"91212129", 9}]
    cases.each do |c|
      got = CrystalDay01.part1(c[0])
      want = c[1]
      got.should eq want
    end
  end

  it "works computing part2" do
    #cases : Array(Tuple(String, Int32))
    cases = [
      {"1212", 6},
      {"1221", 0},
      {"123425", 4},
      {"123123", 12},
      {"12131415", 4},
    ]
    cases.each do |c|
      got = CrystalDay01.part2(c[0])
      want = c[1]
      got.should eq want
    end
  end
end
