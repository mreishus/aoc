#!/usr/bin/env ruby
require 'pp'

#BOARD_SIZE = 11
#FILENAME = 'input_small.txt'

BOARD_SIZE = 1000
FILENAME = 'input.txt'

#BOARD_SIZE = 100000
#FILENAME = 'input_big.txt'

board = Array.new(BOARD_SIZE) { Array.new(BOARD_SIZE, 0) }
File.readlines(FILENAME).each do |line|
  re = '#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
  _, id, x, y, width, length = line.match(re).to_a

  #puts "#{line}"
  #puts "id #{id} x#{x} y#{y} width#{width} length#{length}"

  id = id.to_i
  x = x.to_i
  y = y.to_i
  width = width.to_i
  length = length.to_i

  #puts x + width
  x.upto(x + width - 1) do |xx|
    y.upto(y + length - 1) do |yy|
      #puts "    #{xx},#{yy} add one"
      board[xx][yy] += 1
    end
  end
end

count = 0;
0.upto(BOARD_SIZE - 1) do |x|
  0.upto(BOARD_SIZE - 1) do |y|
    if (board[x][y] > 1)
      #puts "    #{x},#{y} = #{board[x][y]}"
      count += 1
    end
  end
end

puts count
