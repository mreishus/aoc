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
    if a > r[b]
      r[c] = 1
    else
      r[c] = 0
    end
    r
  end

  def gtri(regs, a, b, c)
    r = regs.dup
    if r[a] > b
      r[c] = 1
    else
      r[c] = 0
    end
    r
  end

  def gtrr(regs, a, b, c)
    r = regs.dup
    if r[a] > r[b]
      r[c] = 1
    else
      r[c] = 0
    end
    r
  end

  def eqir(regs, a, b, c)
    r = regs.dup
    if r[a] > b
      r[c] = 1
    else
      r[c] = 0
    end
    r
  end

  def eqri(regs, a, b, c)
    r = regs.dup
    if r[a] == b
      r[c] = 1
    else
      r[c] = 0
    end
    r
  end

  def eqrr(regs, a, b, c)
    r = regs.dup
    if r[a] == r[b]
      r[c] = 1
    else
      r[c] = 0
    end
    r
  end

  def all_instructions
    %w[addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr]
  end
end

require 'pp'

def tests
  raise 'fail0' unless which_opcodes_match([3, 2, 1, 1], [3, 2, 2, 1], 2, 1, 2) == %w[addi mulr seti]
  raise 'fail1' unless how_many_opcodes_match([3, 2, 1, 1], [3, 2, 2, 1], 2, 1, 2) == 3
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

############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

cpu = Compute.new
regs = [3, 2, 1, 1]
pp regs
regs = cpu.public_send('addi', regs, 2, 1, 2)
#regs = cpu.addi(regs, 2, 1, 2)
pp regs

i = cpu.all_instructions
pp i

pp '---------'
#Before: [3, 2, 1, 1]
#9 2 1 2
#After:  [3, 2, 2, 1]
