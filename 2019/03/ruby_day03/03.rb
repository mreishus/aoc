#!/usr/bin/env ruby
require 'pp'

$DIRECTIONS = {
  'R' => Complex(1, 0),
  'L' => Complex(-1, 0),
  'U' => Complex(0, 1),
  'D' => Complex(0, -1)
}

def parse_wire(line)
  dirs = line.split(',')
  a = []
  dirs.each do |dir|
    compass, l = dir.match(/^(\w)(\d+)$/).captures
    a.push([compass, l.to_i])
  end
  a
end

def parse(filename)
  wires = []
  File.readlines(filename).each do |line|
    wire = parse_wire(line)
    wires.push(wire)
  end
  wires
end

def part12(data)
  grid = Hash.new(nil)
  data.each_with_index do |wire, wire_index|
    location = Complex(0, 0)
    total_steps = 0
    wire.each do |step|
      delta = $DIRECTIONS[step[0]]
      1.upto(step[1]) do |i|
        location += delta
        total_steps += 1
        # puts "i #{i} location #{location} wire #{wire_index}"

        if grid[location] == nil
          grid[location] = [
            { wire_index: wire_index, total_steps: total_steps }
          ]
        elsif !grid[location].any? { |thing| thing[:wire_index] == wire_index }
          grid[location].push(
            { wire_index: wire_index, total_steps: total_steps }
          )
        end
      end
    end
  end

  answer1 = 999_999_999
  answer2 = 999_999_999
  grid.each do |key, value|
    next if (value.length < 2)
    distance = key.real.abs + key.imaginary.abs
    # pp key
    # pp value
    # puts "#{key} #{value} #{distance}"
    answer1 = distance if distance < answer1
    step_distance = value.map { |thing| thing[:total_steps] }.sum
    answer2 = step_distance if step_distance < answer2
    # pp '----'
  end

  pp '--answer--'
  [answer1, answer2]
end

data = parse('../input.txt')
# pp data
answers = part12(data)
puts 'Part 1:'
puts answers[0]
puts 'Part 2:'
puts answers[1]
