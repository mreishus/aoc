#!/usr/bin/env ruby
require 'pp'

def parse(filename)
  jumps = []
  File.open(filename).each do |line|
    jumps.push(line.strip().to_i)
  end
  jumps
end

def part1(jumps)
  max = jumps.length

  current_idx = 0
  last_idx = 0
  steps = 0

  loop do
    last_idx = current_idx

    if current_idx >= max
      break
    end

    current_idx += jumps[current_idx]
    jumps[last_idx] += 1
    steps += 1
  end
  steps
end

def part2(jumps)
  max = jumps.length

  current_idx = 0
  last_idx = 0
  steps = 0

  loop do
    last_idx = current_idx

    if current_idx >= max
      break
    end

    current_idx += jumps[current_idx]
    if jumps[last_idx] >= 3
      jumps[last_idx] -= 1
    else
      jumps[last_idx] += 1
    end
    steps += 1
  end
  steps
end

puts "Hello"
jumps = parse("../input_small.txt")
steps = part1(jumps)
puts "Part1 Small: Should equal 5"
puts steps
jumps = parse("../input_small.txt")
steps = part2(jumps)
puts "Part2 Small: Should equal 10"
puts steps

###
puts "\n\n"

jumps = parse("../input.txt")
steps = part1(jumps)
puts "Part1 Large"
puts steps
jumps = parse("../input.txt")
steps = part2(jumps)
puts "Part2 Large"
puts steps

