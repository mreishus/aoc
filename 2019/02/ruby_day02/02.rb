#!/usr/bin/env ruby

require 'pp'

FILENAME = '../input.txt'

def parse(filename)
  nums = []
  File.readlines(FILENAME).each do |line|
    # op, a, b, c = line.strip.match(/(\w+) (\d+) (\d+) (\d+)/).captures
    # if line =~ /^#ip/
    #   ip_index, _ = line.strip.match(/#ip (\d+)/).captures.map(&:to_i)
    #   next
    # end
    nums =
      line.split(',')
    nums = nums.map(&:to_i)
    break
  end
  nums
end

def process(program)
  i = 0
  loop do
    instruction = program[i]
    if instruction == 1
      puts 'add'
      i += 1
      pos1_in = program[i]
      i += 1
      pos2_in = program[i]
      i += 1
      pos_out = program[i]

      ## Addition
      puts "Add #{pos1_in} + #{pos2_in} = #{pos_out}"
      program[pos_out] = program[pos1_in] + program[pos2_in]

      i += 1
    elsif instruction == 2
      puts 'multi'
      i += 1
      pos1_in = program[i]
      i += 1
      pos2_in = program[i]
      i += 1
      pos_out = program[i]

      ## Mult
      puts "Add #{pos1_in} * #{pos2_in} = #{pos_out}"
      program[pos_out] = program[pos1_in] * program[pos2_in]

      i += 1
    elsif instruction == 99
      puts 'Found 99, halting..'
      break
    else
      puts 'Found unexpected instruction'
    end
  end
  puts 'First position:'
  puts program[0]
end

# b = '1,9,10,3,2,3,11,0,99,30,40,50'.split(',').map(&:to_i)
# process(b)

# (You guessed 509871.)
a = parse(FILENAME)
a[1] = 12
a[2] = 2
process(a)
