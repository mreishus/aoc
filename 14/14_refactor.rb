#!/usr/bin/env ruby

require 'pp'

def init
  board = [3, 7]
  e1_select = 0
  e2_select = 1
  [board, e1_select, e2_select]
end

def board_add!(board, e1_select, e2_select)
  sum = ((board[e1_select] + board[e2_select]).to_s.split "").map(&:to_i)
  board.concat sum
end

def move_selections(board, e1_select, e2_select)
  e1_score = board[e1_select]
  e2_score = board[e2_select]
  new_e1_select = (e1_select + 1 + e1_score) % board.length
  new_e2_select = (e2_select + 1 + e2_score) % board.length
  #puts "Board length: #{board.length}"
  #puts "e1_select #{e1_select} e1_score #{e1_score} sum plus one #{e1_select + 1 + e1_score} all done #{new_e1_select}"
  #puts "e2_select #{e2_select} e2_score #{e2_score} sum plus one #{e2_select + 1 + e2_score} all done #{new_e2_select}"
  [new_e1_select, new_e2_select]
end

def part1(target)
  board, e1_select, e2_select = init

  #pp '---'
  #pp board
  #pp e1_select, e2_select

  #1.upto(20) do |z|
  while (board.length <= target+9) do
    board_add! board, e1_select, e2_select


    e1_select, e2_select = move_selections(board, e1_select, e2_select)

    #pp '---'
    #pp board
    #pp e1_select, e2_select
  end

  board[target..(target+9)].map(&:to_s).join("")
end

def part2(target)
  target_string = target.to_s
  board, e1_select, e2_select = init

  result = nil
  while (result == nil) do
    board_add! board, e1_select, e2_select
    e1_select, e2_select = move_selections(board, e1_select, e2_select)

    board_string = board.map(&:to_s).join("")
    search = board_string.index(target_string)
    if search != nil
      result = search
    end
  end
  result
end

def tests
  raise 'fail 1 1' unless part1(9) == "5158916779"
  raise 'fail 1 2' unless part1(5) == "0124515891"
  raise 'fail 1 3' unless part1(18) == "9251071085"
  raise 'fail 1 4' unless part1(2018) == "5941429882"
  raise 'fail 1 5' unless part1(110201) == "6107101544"

  raise 'fail 2 1' unless part2(51589) == 9
  raise 'fail 2 2' unless part2("01245") == 5
  raise 'fail 2 3' unless part2(92510) == 18
  raise 'fail 2 4' unless part2(59414) == 2018
end

tests()

## Main Prog ##

[9, 5, 18, 2018, 110201].each do |x|
  puts "Part 1, target: #{x}"
  puts part1(x)
end

[51589, "01245", 92510, 59414, 110201].each do |x|
  puts "Part 2, target: #{x}"
  puts part2(x)
end
