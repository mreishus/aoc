require "./spec_helper"

describe CrystalDay01 do
  it "works" do
    CrystalDay01.fuel(12).should eq 2
    CrystalDay01.fuel(14).should eq 2
		CrystalDay01.fuel(1_969).should eq 654
		CrystalDay01.fuel(100_756).should eq 33_583
		CrystalDay01.total_fuel(14).should eq 2
		CrystalDay01.total_fuel(1_969).should eq 966
		CrystalDay01.total_fuel(100_756).should eq 50_346
  end
end
