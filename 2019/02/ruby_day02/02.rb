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
      #puts 'add'
      i += 1
      pos1_in = program[i]
      i += 1
      pos2_in = program[i]
      i += 1
      pos_out = program[i]

      ## Addition
      #puts "Add #{pos1_in} + #{pos2_in} = #{pos_out}"
      program[pos_out] = program[pos1_in] + program[pos2_in]

      i += 1
    elsif instruction == 2
      #puts 'multi'
      i += 1
      pos1_in = program[i]
      i += 1
      pos2_in = program[i]
      i += 1
      pos_out = program[i]

      ## Mult
      #puts "Add #{pos1_in} * #{pos2_in} = #{pos_out}"
      program[pos_out] = program[pos1_in] * program[pos2_in]

      i += 1
    elsif instruction == 99
      # puts 'Found 99, halting..'
      break
    else
      puts 'Found unexpected instruction'
    end
  end
  # puts 'First position:'
  # puts program[0]
  program[0]
end

# b = '1,9,10,3,2,3,11,0,99,30,40,50'.split(',').map(&:to_i)
# process(b)

# Incorrect p1: (You guessed 509871.)  (Forgot to replace)
a = parse(FILENAME)
a[1] = 12
a[2] = 2
puts 'Part 1:'
puts process(a)

# p2
# to determine what pair of inputs produces the output 19690720."
# a[1] = noun 0-99
# a[2] = verb 0-99

0.upto(99) do |xx|
  0.upto(99) do |yy|
    a = parse(FILENAME)
    a[1] = xx
    a[2] = yy
    l = process(a)
    if l == 19_690_720
      puts "noun: #{xx}"
      puts "verb: #{yy}"
      puts "Part 2: 100 * noun + verb: #{100 * xx + yy}"
      exit
    end
  end
end
