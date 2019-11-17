#!/usr/bin/env ruby
require 'pp'

def removes(string)
  indexes = []
  string.each_char.with_index do |item, index|
    this_char = item
    next_char = string[index + 1]
    ##puts "index of #{item}: #{index}.  Next? #{string[index + 1]}"
    if next_char != nil && this_char != next_char &&
         this_char.downcase == next_char.downcase
      indexes.push(index)
    end
  end
  return indexes.reverse
end

def react(data)
  z = removes(data)

  while z.length > 0
    last_i = 0
    z.each do |i|
      next if i == last_i - 1
      a = data[0, i]
      b = data[i + 2, data.length]
      #puts "-------[#{i}"
      #puts data
      data = a + b
      #puts data[i,i+2]
      #puts data
      #puts '------'
      last_i = i
    end
    #puts data

    z = removes(data)
  end
  data
end

orig_data = File.read('input.txt').strip
## Part 1
puts react(orig_data).length

## Part 2
lens = []
('a'..'z').each do |letter|
  pp letter
  bothletters = letter + letter.upcase
  this_length = react(orig_data.tr(bothletters, '')).length
  #puts "#{letter} #{this_length}"
  lens.push this_length
end

puts lens.min
