#!/usr/bin/env ruby

require 'pp'

def init
  board = [3, 7]
  e1_select = 0
  e2_select = 1
  [board, e1_select, e2_select]
end

def board_add!(board, e1_select, e2_select)
  new_elements_string = (board[e1_select] + board[e2_select]).to_s
  sum = (new_elements_string.split '').map(&:to_i)
  board.concat sum
  new_elements_string
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

  while (board.length <= target + 9)
    board_add! board, e1_select, e2_select
    e1_select, e2_select = move_selections(board, e1_select, e2_select)
  end

  board[target..(target + 9)].map(&:to_s).join('')
end

def part2(target)
  target_string = target.to_s
  board, e1_select, e2_select = init
  board_string = board.map(&:to_s).join('')

  offset = 0

  result = nil
  while (result == nil)
    new_elements_string = board_add! board, e1_select, e2_select
    e1_select, e2_select = move_selections(board, e1_select, e2_select)

    board_string += new_elements_string
    search = board_string.index(target_string)
    result = search + offset if search != nil

    if board_string.length > 30
      shorten_amount = 20
      board_string = board_string[shorten_amount..-1]
      offset += shorten_amount
    end
  end
  result
end

def tests
  raise 'fail 1 1' unless part1(9) == '5158916779'
  raise 'fail 1 2' unless part1(5) == '0124515891'
  raise 'fail 1 3' unless part1(18) == '9251071085'
  raise 'fail 1 4' unless part1(2_018) == '5941429882'
  raise 'fail 1 5' unless part1(110_201) == '6107101544'

  raise 'fail 2 1' unless part2(51_589) == 9
  raise 'fail 2 2' unless part2('01245') == 5
  raise 'fail 2 3' unless part2(92_510) == 18
  raise 'fail 2 4' unless part2(59_414) == 2_018
end

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

## Main Prog ##

[9, 5, 18, 2_018, 110_201].each do |x|
  puts "Part 1, target: #{x}"
  puts part1(x)
end

[51_589, '01245', 92_510, 59_414, 110_201].each do |x|
  puts "Part 2, target: #{x}"
  puts part2(x)
end
