#!/usr/bin/env ruby

require 'pp'

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

def tests
  p1_tests
  opcode_tests
end

def p1_tests
  raise 'fail p1 small' unless part1('input_small.txt') == 7
  # Too slow:
  #raise 'fail p1 medium' unless 912 == part1('input.txt')
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
  regs_before = [0, 0, 3, 0, 98, 99]
  regs_after = cpu.public_send('eqir', regs_before, 3, 2, 3)
  regs_expect = [0, 0, 3, 1, 98, 99]
  raise 'fail3' unless regs_after == regs_expect
end

def parse_file(filename)
  program = []
  ip_index = -1
  File.readlines(filename).each do |line|
    puts line
    if line =~ /^#ip/
      ip_index, _ = line.strip.match(/#ip (\d+)/).captures.map(&:to_i)
      next
    end
    op, a, b, c = line.strip.match(/(\w+) (\d+) (\d+) (\d+)/).captures
    instruction = { op: op, a: a.to_i, b: b.to_i, c: c.to_i }
    program.push instruction
  end
  { program: program, ip_index: ip_index, regs: [0, 0, 0, 0, 0, 0] }
end

def tick(data)
  program, ip_index, regs = data.values_at(:program, :ip_index, :regs)

  to_execute = program[regs[ip_index]]
  op, a, b, c = to_execute.values_at(:op, :a, :b, :c)

  cpu = Compute.new
  new_regs = cpu.public_send(op, regs, a, b, c)
  new_regs[ip_index] += 1

  { program: program, ip_index: ip_index, regs: new_regs }
end

def invalid_ip(data)
  program, ip_index, regs = data.values_at(:program, :ip_index, :regs)
  to_execute = program[regs[ip_index]]
  to_execute.nil?
end

def part1(filename)
  data = parse_file(filename)

  loop do
    data = tick(data)
    #pp data[:regs]
    break if invalid_ip(data)
  end
  #pp data[:regs]
  #puts "Left in reg 0: " 
  #puts data[:regs][0]
  data[:regs][0]
end

############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

filename = 'input_small.txt'
filename = 'input.txt'
answer = part1(filename)
pp answer

=begin
filename = 'input.txt'
data = parse_file(filename)

loop do
  data = tick(data)
  #pp data[:regs]
  break if invalid_ip(data)
end
pp data[:regs]
puts "Left in reg 0: " 
puts data[:regs][0]
=end
