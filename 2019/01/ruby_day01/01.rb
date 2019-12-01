#!/usr/bin/env ruby

def parse_file(filename)
  nums = []
  File.readlines(filename).each do |line|
    num = line.strip.to_i
    nums.push(num)
  end
  nums
end

def part1(filename)
  parse_file(filename).map { |num| part1_fuel_for_num(num) }.reduce(:+)
end

def part1_fuel_for_num(num)
  (num / 3) - 2
end

def part2(filename)
  parse_file(filename).map { |num| part2_fuel_for_num(num) }.reduce(:+)
end

def part2_fuel_for_num(num)
  total_fuel = 0
  fuel = num
  loop do
    fuel = (fuel / 3) - 2
    if (fuel >= 0)
      total_fuel += fuel
    else
      break
    end
  end
  total_fuel
end

puts 'AOC 2019 Day 01'
# Part 1
puts 'Part 1 answer:'
puts part1('../input.txt')

# Part 2
puts 'Part 2 answer:'
puts part2('../input.txt')
