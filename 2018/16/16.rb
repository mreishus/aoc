#!/usr/bin/env ruby

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

class Compute
  def addr(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] + r[b]
    r
  end

  def addi(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] + b
    r
  end

  def mulr(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] * r[b]
    r
  end

  def muli(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] * b
    r
  end

  def banr(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] & r[b]
    r
  end

  def bani(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] & b
    r
  end

  def borr(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] | r[b]
    r
  end

  def bori(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] | b
    r
  end

  def setr(regs, a, _b, c)
    r = regs.dup
    r[c] = r[a]
    r
  end

  def seti(regs, a, _b, c)
    r = regs.dup
    r[c] = a
    r
  end

  def gtir(regs, a, b, c)
    r = regs.dup
    r[c] = a > r[b] ? 1 : 0
    r
  end

  def gtri(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] > b ? 1 : 0
    r
  end

  def gtrr(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] > r[b] ? 1 : 0
    r
  end

  def eqir(regs, a, b, c)
    r = regs.dup
    r[c] = a == r[b] ? 1 : 0
    r
  end

  def eqri(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] == b ? 1 : 0
    r
  end

  def eqrr(regs, a, b, c)
    r = regs.dup
    r[c] = r[a] == r[b] ? 1 : 0
    r
  end

  def all_instructions
    %w[addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr]
  end
end

require 'pp'

def tests
  opcode_tests
  p2_tests
  raise 'fail0' unless which_opcodes_match([3, 2, 1, 1], [3, 2, 2, 1], 2, 1, 2) == %w[addi mulr seti]
  raise 'fail1' unless how_many_opcodes_match([3, 2, 1, 1], [3, 2, 2, 1], 2, 1, 2) == 3
  raise 'fail2' unless part1('input_1.txt') == 570
end

def p2_tests
  opcodes = determine_opcodes('input_1.txt')
  regs = part2('input_2.txt', opcodes)
  raise 'fail p2' unless regs[0] == 503
end

def opcode_tests
  # A = 3  Value A = 3  Register A = 0
  # B = 2  Value B = 2  Register B = 3
  # C = 3
  # Something that sets register 3.
  # Before: [0, 0, 3, 0]
  # 14 3 2 3
  # After:  [0, 0, 3, 1]

  cpu = Compute.new
  regs_before = [0, 0, 3, 0]
  regs_after = cpu.public_send('eqir', regs_before, 3, 2, 3)
  regs_expect = [0, 0, 3, 1]
  raise 'fail3' unless regs_after == regs_expect
end

def which_opcodes_match(regs_before, regs_after, a, b, c)
  matches = []
  cpu = Compute.new
  cpu.all_instructions.each do |method_name|
    matches.push method_name if cpu.public_send(method_name, regs_before, a, b, c) == regs_after
  end
  matches.sort
end

def how_many_opcodes_match(regs_before, regs_after, a, b, c)
  which_opcodes_match(regs_before, regs_after, a, b, c).count
end

def parse_mystery_input(filename)
  mystery_inputs = []
  File.open(filename, 'r') do |fh|
    loop do
      line = fh.gets
      break if line.nil?

      before_regs = line.strip.match(/Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]/).captures.map(&:to_i)

      line = fh.gets
      break if line.nil?

      opcode, a, b, c = line.strip.match(/(\d+) (\d+) (\d+) (\d+)/).captures.map(&:to_i)

      line = fh.gets
      break if line.nil?

      after_regs = line.strip.match(/After:\s+\[(\d+), (\d+), (\d+), (\d+)\]/).captures.map(&:to_i)

      mystery_input = { before_regs: before_regs, after_regs: after_regs, opcode: opcode, a: a, b: b, c: c }
      mystery_inputs.push mystery_input

      # Blank line
      line = fh.gets
      break if line.nil?
    end
  end
  mystery_inputs
end

def part1(filename)
  how_many_behave_like_three_or_more = 0
  mystery_inputs = parse_mystery_input(filename)
  mystery_inputs.each do |x|
    matches = how_many_opcodes_match(x[:before_regs], x[:after_regs], x[:a], x[:b], x[:c])
    how_many_behave_like_three_or_more += 1 if matches >= 3
  end
  how_many_behave_like_three_or_more
end

def part2(filename, opcodes)
  cpu = Compute.new
  instructions = parse_program_file(filename)
  regs = [0, 0, 0, 0]
  instructions.each do |i|
    opcode = opcodes[i[:opcode]]
    raise "Invalid opcode" if opcode.nil?

    regs = cpu.public_send(opcode, regs, i[:a], i[:b], i[:c])
  end
  regs
end

def parse_program_file(filename)
  instructions = []
  File.readlines(filename).each do |line|
    opcode, a, b, c = line.strip.match(/(\d+) (\d+) (\d+) (\d+)/).captures.map(&:to_i)
    instruction = { opcode: opcode, a: a, b: b, c: c }
    instructions.push instruction
  end
  instructions
end

def determine_opcodes(filename)
  opcode_defs = {}
  mystery_inputs = parse_mystery_input(filename)
  mystery_inputs.each do |x|
    matches = which_opcodes_match(x[:before_regs], x[:after_regs], x[:a], x[:b], x[:c])
    if opcode_defs.key?(x[:opcode])
      opcode_defs[x[:opcode]] &= matches # Array Intersection
    else
      opcode_defs[x[:opcode]] = matches
    end
  end

  0.upto(20) do
    opcode_defs = deduce(opcode_defs)
  end
  if opcode_defs.values.select { |x| x.count > 1 }.any?
    raise 'Failed to figure out opcodes..'
  end

  opcode_defs.keys.each do |x|
    opcode_defs[x] = opcode_defs[x].first
  end
  opcode_defs
end

# Deduce: Loop for opcodes with only one possible meaning and
# remove that meaning from others
# Example Input: { 1 => ["add", "multiply"], 2 => ["multiply"] }
# 1 must be add, because 2 is already multiply...
# Example Output: { 1 => ["add"], 2 => ["multiply"] }
def deduce(opcode_defs)
  opcodes_with_one_definition(opcode_defs).each do |opcode|
    opcode_defs.keys.reject { |x| x == opcode }.each do |x|
      opcode_defs[x].reject! { |y| y == opcode_defs[opcode].first }
    end
  end
  opcode_defs
end

def opcodes_with_one_definition(opcode_defs)
  opcode_defs.keys.select { |x| opcode_defs[x].length == 1 }
end

############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

puts 'How many behave like 3 or more opcodes (Part 1) '
puts part1('input_1.txt')

puts 'Let\'s figure out the opcodes'
opcodes = determine_opcodes('input_1.txt')
puts 'Part2, running program...'
regs = part2('input_2.txt', opcodes)
puts 'Part2: All registers...'
pp regs
