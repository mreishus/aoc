#!/usr/bin/env ruby

def parse_file(filename)
  File.readlines(filename).map { |line| line.strip.to_i }
end

def part1(filename)
  parse_file(filename).map { |num| fuel(num) }.reduce(:+)
end

def fuel(num)
  (num / 3) - 2
end

def part2(filename)
  parse_file(filename).map { |num| total_fuel(num) }.reduce(:+)
end

def total_fuel(num)
  total_fuel = 0
  fuel = num
  loop do
    fuel = (fuel / 3) - 2
    break if fuel <= 0
    total_fuel += fuel
  end
  total_fuel
end

def tests
  raise 'fail1' unless fuel(12) == 2
  raise 'fail2' unless fuel(14) == 2
  raise 'fail3' unless fuel(1_969) == 654
  raise 'fail4' unless fuel(100_756) == 33_583
  raise 'fail5' unless total_fuel(14) == 2
  raise 'fail6' unless total_fuel(1_969) == 966
  raise 'fail7' unless total_fuel(100_756) == 50_346
end

tests
puts 'All tests completed!'

puts 'AOC 2019 Day 01'
# Part 1
puts 'Part 1 answer:'
puts part1('../input.txt')

# Part 2
puts 'Part 2 answer:'
puts part2('../input.txt')
