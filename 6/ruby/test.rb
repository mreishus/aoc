#!/usr/bin/env ruby
require 'pp'

FILENAME = 'input.txt'
SAFE_THRES = 10000
#FILENAME = 'input_small.txt'
#SAFE_THRES = 32

def find_closest(coords, x, y)
  answers = []
  i = 1
  coords.each do |coord|
    dist = distance(x, y, coord[0], coord[1])
    #puts "#{x} #{y}    #{coord[0]} #{coord[1]} = #{dist}"

    answers.push({"coord" => i, "dist" => distance(x, y, coord[0], coord[1]) })
    i += 1
  end
  answers = answers.sort_by {|z| z["dist"]}   #=> "dog"
  
  rval = -1 #tie
  if answers[0]["dist"] != answers[1]["dist"]
    rval = answers[0]["coord"]
  end
  #puts '---'
  #puts "#{x}, #{y}"
  #puts answers
  #puts rval
  #puts '---'
  rval
end

def distance(x1, y1, x2, y2)
  (x1 - x2).abs + (y1 - y2).abs
end


coords = []
File.readlines(FILENAME).each do |line|
  a = line.strip.split(", ")
  a[0] = a[0].to_i
  a[1] = a[1].to_i
  coords.push a
end

xs = coords.map{ |x| x[0] }
ys = coords.map{ |x| x[1] }
max_x = xs.max
max_y = ys.max
pp coords
pp max_x
pp max_y
BOARD_SIZE_X = max_x + 1
BOARD_SIZE_Y = max_y + 1
board = Array.new(BOARD_SIZE_X + 1) { Array.new(BOARD_SIZE_Y + 1, 0) }
0.upto(BOARD_SIZE_X) do |x|
  0.upto(BOARD_SIZE_Y) do |y|
    board[x][y] = {:is_coord => nil, :assigned_coord => nil, :is_inf => false}
  end
end

i = 1
coords.each do |coord|
  x = coord[0]
  y = coord[1]
  board[x][y] = {:is_coord => i, :assigned_coord => nil, :is_inf => false}
  i += 1
end

0.upto(BOARD_SIZE_X) do |x|
  0.upto(BOARD_SIZE_Y) do |y|
    board[x][y][:assigned_coord] = find_closest(coords, x, y)

    if (x == 0 || y == 0 || x == BOARD_SIZE_X || y == BOARD_SIZE_Y)
      board[x][y][:is_inf] = true
    end

    #pp board[x][y]
  end
end

area_calcs = []
i = 1
coords.each do |coord|
  # Is it infinite?
  is_infinite = false
  size = 0
  0.upto(BOARD_SIZE_X) do |x|
    0.upto(BOARD_SIZE_Y) do |y|
      if board[x][y][:assigned_coord] == i
        size += 1
        if board[x][y][:is_inf]
          is_infinite = true
        end
      end
    end
  end

  puts "Coord: #{i} Infinite: #{is_infinite} Size #{size}"
  area_calcs.push({"coord" => i, "size" => size, "is_infinite" => is_infinite })
  i += 1
end

0.upto(BOARD_SIZE_Y) do |y|
  0.upto(BOARD_SIZE_X) do |x|
    print board[x][y][:assigned_coord]
    print board[x][y][:is_inf] ? 'i' : '.'
    print " "
  end
  print "\n"
end

pp area_calcs
non_inf_areas = area_calcs.select {|z| !z["is_infinite"] }
pp '--'
winner = non_inf_areas.max_by {|z| z["size"]}
pp winner
puts "Part 1 answer: "
pp winner["size"]

## Now let's find safe
# SAFE_THRES
safe_squares = 0
0.upto(BOARD_SIZE_Y) do |y|
  0.upto(BOARD_SIZE_X) do |x|
    total_distance = 0

    coords.each do |coord|
      total_distance += distance(x, y, coord[0], coord[1])
    end

    if total_distance < SAFE_THRES
      safe_squares += 1
    end
    
  end
end

puts "Part 2, numbe rof safe squares"
pp safe_squares

## :(
## I guessed 25174 and it was incorrect.
