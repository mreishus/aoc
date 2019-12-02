#!/usr/bin/env ruby

require 'pp'

FILENAME = '../input.txt'

def parse(filename)
  File.readlines(FILENAME).first.split(',').map(&:to_i)
end

def process(program)
  i = 0
  loop do
    instruction = program[i]
    if instruction == 1
      ## Addition
      pos1_in = program[i + 1]
      pos2_in = program[i + 2]
      pos_out = program[i + 3]
      i += 4

      #puts "Add #{pos1_in} + #{pos2_in} = #{pos_out}"
      program[pos_out] = program[pos1_in] + program[pos2_in]
    elsif instruction == 2
      ## Mult
      pos1_in = program[i + 1]
      pos2_in = program[i + 2]
      pos_out = program[i + 3]
      i += 4

      #puts "Add #{pos1_in} * #{pos2_in} = #{pos_out}"
      program[pos_out] = program[pos1_in] * program[pos2_in]
    elsif instruction == 99
      # puts 'Found 99, halting..'
      break
    else
      raise 'Failing after unexpected instruction'
    end
  end
  program
end

def part1(program)
  p = program.clone
  p[1] = 12
  p[2] = 2
  p = process(p)
  p[0]
end

def part2(program)
  # to determine what pair of inputs produces the output 19690720."
  # a[1] = noun 0-99
  # a[2] = verb 0-99
  0.upto(99) do |xx|
    0.upto(99) do |yy|
      p = program.clone
      p[1] = xx
      p[2] = yy
      p = process(p)
      if p[0] == 19_690_720
        # puts "noun: #{xx}"
        # puts "verb: #{yy}"
        # puts "Part 2: 100 * noun + verb: #{100 * xx + yy}"
        return 100 * xx + yy
      end
    end
  end
end

a = parse(FILENAME)
puts 'Part 1:'
puts part1(a)
puts 'Part 2:'
puts part2(a)
