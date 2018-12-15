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

  puts "answer:"
  puts board[target..(target+9)].map(&:to_s).join("")
end

[9, 5, 18, 2018, 110201].each do |x|
  puts "Part 1, target: #{x}"
  part1(x)
  puts ""
end