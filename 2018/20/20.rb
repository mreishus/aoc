#!/usr/bin/env ruby

require 'pp'
class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

def tests
end

def parse(filename)
  chars = File.read(filename).strip
  raise 'Invalid file beginning' unless chars[0] == '^'
  raise 'Invalid file ending' unless chars[chars.length-1] == '$'

  chars[0] = ''
  chars.chomp('$')
end

def parse2(filename)
  positions = []
  distance = 0
  distance_for_position = Hash.new(0)
  current_position = Complex(0, 0)

  chars = parse(filename)
  chars.each_char do |x|
    if x == '('
      positions.push(current_position)
    elsif x == ')'
      current_position = positions.pop
    elsif x == '|'
      current_position = positions[-1]
    elsif %w[N E S W].include? x
      distance += 1
      new_position = change_position(current_position, x)

      compare_these = [
        distance_for_position[current_position] + 1
      ]
      if distance_for_position.key?(new_position)
        compare_these.push(distance_for_position[new_position])
      end

      distance_for_position[new_position] = compare_these.min
      current_position = new_position
    end
  end
  distance_for_position
end

def change_position(current_position, letter)
  return current_position + Complex(0, 1) if letter == 'N'
  return current_position + Complex(0, -1) if letter == 'S'
  return current_position + Complex(-1, 0) if letter == 'W'
  return current_position + Complex(1, 0) if letter == 'E'

  current_position
end

def part1(filename)
  distances = parse2(filename)
  distances.values.max
end

def part2(filename)
  distances = parse2(filename)
  distances.values.select { |x| x >= 1000 }.count
end

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

filename = 'input.txt'
puts part1(filename)
puts part2(filename)

