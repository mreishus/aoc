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
  chars = parse(filename)

  top_array = [[]]
  this_array = top_array

  array_stack = [top_array]
  i_stack = []

  pp chars
  i = 0
  chars.each_char do |x|
    if %w[N E W S].include? x
      if this_array[i].nil?
        this_array[i] = []
      end
      this_array[i].push x
    elsif x == '('
      i_stack.push i
      newa = []
      this_array[i].push newa
      array_stack.push this_array
      this_array = newa

      i = 0
      #pp '++'
      #pp top_array
    elsif x == ')'
      this_array = array_stack.pop
      i = i_stack.pop
    elsif x == '|'
      this_array.push []
      i += 1
    end
  end
  top_array[0]
end

def part1(filename)
  paths_array = parse2(filename)
end

############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

filename = 'input_tiny.txt'
part1(filename)
