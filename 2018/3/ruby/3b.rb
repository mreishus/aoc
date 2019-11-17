#!/usr/bin/env ruby
require 'pp'

#BOARD_SIZE = 11
#FILENAME = 'input_small.txt'

BOARD_SIZE = 1_000
FILENAME = 'input.txt'

#BOARD_SIZE = 100000
#FILENAME = 'input_big.txt'

board = Array.new(BOARD_SIZE) { Array.new(BOARD_SIZE, nil) }
all_ids = []
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
      board[xx][yy] = [] if (board[xx][yy].nil?) # Workaround to not init 3d array correctly
      #puts "    #{xx},#{yy} add one"
      board[xx][yy].push(id)
    end
  end

  all_ids.push id
end

non_overlapping_ids = all_ids

#puts "3,3"
#pp board[3][3]
#puts "3,2"
#pp board[3][2]

0.upto(BOARD_SIZE - 1) do |x|
  0.upto(BOARD_SIZE - 1) do |y|
    if (!board[x][y].nil? && board[x][y].length > 1)
      non_overlapping_ids -= board[x][y]
    end
  end
end

puts 'Non overlapping ids:'
pp non_overlapping_ids
#puts count
