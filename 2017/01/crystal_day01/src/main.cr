require "./crystal_day01"
text = File.read("../input.txt").chomp
puts "Part1: "
puts CrystalDay01.part1(text)
puts "Part2: "
puts CrystalDay01.part2(text)
