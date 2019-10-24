#!/usr/bin/env ruby

require 'pp'

#FILENAME = 'input.txt'
FILENAME = 'input_small.txt'

#stars = []
#File.readlines(FILENAME).each do |line|
#  posx, posy, velx, vely = line
#    .match(/position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>/i)
#    .captures.map{ |x| x.to_i }
#  star = {posx: posx, posy: posy, velx: velx, vely: vely}
#  stars.push(star)
#end

class Grid
  def self.calc(x, y, serial)
    @grid_calculations ||= Hash.new do |h, key|
      x = key[0]
      y = key[1]
      serial = key[2]
      rack_id = x + 10
      power = ((rack_id * y) + serial) * rack_id
      hundreds = ((power/ 100) % 10).floor
      h[key] = hundreds - 5
    end
    @grid_calculations[[x, y, serial]]
  end
end

raise "fail1" unless Grid.calc(3,5,8) == 4;
raise "fail2" unless Grid.calc(122,79,57) == -5;
raise "fail3" unless Grid.calc(217,196,39) == 0;
raise "fail4" unless Grid.calc(101,153,71) == 4;
raise "fail5" unless Grid.calc(3,5,8) == 4;
raise "fail6" unless Grid.calc(122,79,57) == -5;
raise "fail7" unless Grid.calc(217,196,39) == 0;
raise "fail8" unless Grid.calc(101,153,71) == 4;
puts "Passed tests"


puts "Part 1"
max_val = 0
max_x = -1
max_y = -1
serial = 1308

(1).upto(300-3) do |y|
  (1).upto(300-3) do |x|
    val = 0
    (0).upto(2) do |yadd|
      (0).upto(2) do |xadd|
        val += Grid.calc(x + xadd, y+yadd, serial)
      end
    end
    if (max_val < val)
      max_val = val
      max_x = x
      max_y = y
      puts "New Max #{max_val} (#{max_x}, #{max_y})"
    end
  end
end

puts "Part 2"
max_val = 0
max_x = -1
max_y = -1
serial = 1308
#size = 3

(1).upto(300) do |size|
(1).upto(300-size) do |y|
  (1).upto(300-size) do |x|
    val = 0
    (0).upto(size-1) do |yadd|
      (0).upto(size-1) do |xadd|
        val += Grid.calc(x + xadd, y+yadd, serial)
      end
    end
    if (max_val < val)
      max_val = val
      max_x = x
      max_y = y
      max_size = size
      puts "New Max #{max_val} (#{max_x}, #{max_y}, #{size})"
    end
  end
end
end

## Failed Guesses
# 235,86,13
