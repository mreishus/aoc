#!/usr/bin/env ruby

require 'pp'

def extend_left(state, xoffset)
  if state[0] == '#'
    return '..' + state, xoffset - 2
  elsif state[1] == '#'
    return '.' + state, xoffset - 1
  end
  [state, xoffset]
end

def extend_right(state)
  if state[state.length - 1] == '#'
    return state + '..'
  elsif state[state.length - 2] == '#'
    return state + '.'
  end
  state
end

def extend(state, xoffset)
  extend_left(extend_right(state), xoffset)
end

def new_state(state, map, xoffset)
  state, xoffset = extend(state, xoffset)
  new_state = ''

  range = 0..(state.length - 1)
  range.each do |x|
    parent_string = ''
    (-2).upto(2) do |z|
      look_i = x + z
      if range.include?(look_i)
        parent_string += state[look_i]
      else
        parent_string += '.'
      end
    end
    #puts parent_string

    if map.has_key?(parent_string)
      new_state += map[parent_string]
    else
      new_state += '.'
    end
  end

  [new_state, xoffset]
end

def getcount(state, xoffset)
  count = 0
  state.chars.each_with_index { |c, i| count += (i + xoffset) if c == '#' }
  count
end

FILENAME = 'input.txt'
#FILENAME = 'input_small.txt'

lines = File.readlines(FILENAME)
initial_state = lines.shift.strip
lines.shift

initial_state, _ = initial_state.match(/initial state: ([#\.]+)/).captures
map = {}
lines.each do |line|
  left, right = line.strip.match(/([\.#]+) => ([#\.])/).captures
  map[left] = right
end

state = initial_state
xoffset = 0
pp state
#1.upto(20) do |x|
last_count = 0
1.upto(50_000_000_000) do |x|
  state, xoffset = new_state(state, map, xoffset)
  if x % 1_000 == 0
    puts x
    new_count = getcount(state, xoffset)
    puts "#{new_count}  diff #{new_count - last_count}"
    how_many_more = (50_000_000_000 - x) / 1_000
    #/ 1000) * (new_count-last_count)
    puts " hmm... estimate: #{
           (how_many_more * (new_count - last_count)) + new_count
         }"
    last_count = new_count
  end
  #pp state
end

## 9699999999321 # Blank line
