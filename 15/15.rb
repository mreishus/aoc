#!/usr/bin/env ruby

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

require 'pp'

def tests
  raise 'fail' unless true == true
end

def readfile(filename)
  max_x, max_y = readfile_coords(filename)
  grid = Array.new(max_x+1) { Array.new(max_y + 1)}
  units = []
  y = 0
  File.readlines(filename).each do |line|
    x = 0
    line.chars.each do |c|
      x += 1
      if c == '#'
        grid[x][y] = '#'
      elsif c == 'G'
        grid[x][y] = '.'
        unit = {x: x, y: y, type: 'gob', display: 'G'}
        units.push unit
      elsif c == 'E'
        grid[x][y] = '.'
        unit = {x: x, y: y, type: 'elf', display: 'E'}
        units.push unit
      elsif c == '.'
        grid[x][y] = '.'
      end
    end
    y += 1
  end
  [grid, units, max_x, max_y]
end

# Gets max_x and max_y, 0 indexed, from file
def readfile_coords(filename)
  max_x = 0
  max_y = 0
  y = 0
  File.readlines(filename).each do |line|
    line = line.strip
    max_x = [max_x, line.length].max
    y += 1
  end
  max_y = y
  [max_x, max_y]
end

def display(grid, units, max_x, max_y)
  0.upto(max_y) do |y|
    0.upto(max_x) do |x|
      #puts "x [#{x}]"
      unit = units.find{ |u| x.to_i == u[:x] && y.to_i == u[:y] }
      print unit == nil ? grid[x][y] : unit[:display]
    end
    print "\n"
  end
end

def part1(filename)
  grid, units, max_x, max_y = readfile(filename)
  display(grid, units, max_x, max_y)
end

begin_tests = Time.now
tests()
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

["input_small.txt"].each do |x|
  puts "Part 1, target: #{x}"
  part1(x)
end
