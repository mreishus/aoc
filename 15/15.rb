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
  unit_id = 0
  y = 0
  File.readlines(filename).each do |line|
    x = 0
    line.chars.each do |c|
      x += 1
      if c == '#'
        grid[x][y] = '#'
      elsif c == 'G'
        grid[x][y] = '.'
        unit = {x: x, y: y, type: 'gob', display: 'G', id: unit_id}
        unit_id += 1
        units.push unit
      elsif c == 'E'
        grid[x][y] = '.'
        unit = {x: x, y: y, type: 'elf', display: 'E', id: unit_id}
        unit_id += 1
        units.push unit
      elsif c == '.'
        grid[x][y] = '.'
      end
    end
    y += 1
  end
  {grid: grid, units: units, max_x: max_x, max_y: max_y}
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

def display(gamedata)
  grid, units, max_x, max_y = gamedata.values_at(:grid, :units, :max_x, :max_y)

  0.upto(max_y) do |y|
    0.upto(max_x) do |x|
      #puts "x [#{x}]"
      unit = units.find{ |u| x.to_i == u[:x] && y.to_i == u[:y] }
      print unit == nil ? grid[x][y] : unit[:display]
    end
    print "\n"
  end
end

def tick(input_gamedata)
  gamedata = input_gamedata.dup
  units = gamedata[:units]
  turn_order = units.sort_by {|h| [ h[:y].to_i, h[:x].to_i ]}.map {|u| u[:id] }
  turn_order.each do |id| 
    gamedata = tick_unit(gamedata, id)
  end
  gamedata
end

def tick_unit(input_gamedata, id)
  gamedata = input_gamedata.dup
  unit = gamedata[:units].find{ |u| u[:id] == id }
  unit[:x] += 1
  gamedata
end

def part1(filename)
  gamedata = readfile(filename)
  display(gamedata)
  gamedata = tick(gamedata)
  display(gamedata)
end

begin_tests = Time.now
tests()
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

["input_small.txt"].each do |x|
  puts "Part 1, target: #{x}"
  part1(x)
end
