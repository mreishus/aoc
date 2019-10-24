#!/usr/bin/env ruby

require 'pp'
require 'io/console'

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

class Compute
  def addr(r, a, b, c)
    r[c] = r[a] + r[b]
    r
  end

  def addi(r, a, b, c)
    r[c] = r[a] + b
    r
  end

  def mulr(r, a, b, c)
    r[c] = r[a] * r[b]
    r
  end

  def muli(r, a, b, c)
    r[c] = r[a] * b
    r
  end

  def banr(r, a, b, c)
    r[c] = r[a] & r[b]
    r
  end

  def bani(r, a, b, c)
    r[c] = r[a] & b
    r
  end

  def borr(r, a, b, c)
    r[c] = r[a] | r[b]
    r
  end

  def bori(r, a, b, c)
    r[c] = r[a] | b
    r
  end

  def setr(r, a, _b, c)
    r[c] = r[a]
    r
  end

  def seti(r, a, _b, c)
    r[c] = a
    r
  end

  def gtir(r, a, b, c)
    r[c] = a > r[b] ? 1 : 0
    r
  end

  def gtri(r, a, b, c)
    r[c] = r[a] > b ? 1 : 0
    r
  end

  def gtrr(r, a, b, c)
    r[c] = r[a] > r[b] ? 1 : 0
    r
  end

  def eqir(r, a, b, c)
    r[c] = a == r[b] ? 1 : 0
    r
  end

  def eqri(r, a, b, c)
    r[c] = r[a] == b ? 1 : 0
    r
  end

  def eqrr(r, a, b, c)
    r[c] = r[a] == r[b] ? 1 : 0
    r
  end

  def all_instructions
    %w[addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr]
  end
end

def tests
  #p1_tests
  #opcode_tests
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
    if line =~ /^#ip/
      ip_index, _ = line.strip.match(/#ip (\d+)/).captures.map(&:to_i)
      next
    end
    op, a, b, c = line.strip.match(/(\w+) (\d+) (\d+) (\d+)/).captures
    instruction = { op: op, a: a.to_i, b: b.to_i, c: c.to_i }
    program.push instruction
  end
  { program: program, ip_index: ip_index, regs: [1, 0, 0, 0, 0, 0] }
end

def tick(data)
  program, ip_index, regs = data.values_at(:program, :ip_index, :regs)

  to_execute = program[regs[ip_index]]
  op, a, b, c = to_execute.values_at(:op, :a, :b, :c)

  optimize_8000000 = regs[ip_index] == 10 \
    && ( \
      (regs[5]*regs[2]+(8000010/regs[2])) < regs[1] \
      || (regs[5] * regs[2] > regs[1] && regs[5] < regs[1]) \
    ) && regs[3] == 0
  optimize_800000 = regs[ip_index] == 10 && (regs[5]*regs[2]+(800010/regs[2])) < regs[1] && regs[3] == 0
  optimize_70000 = regs[ip_index] == 10 && (regs[5]*regs[2]+(70010/regs[2])) < regs[1] && regs[3] == 0
  optimize_6000 = regs[ip_index] == 10 && (regs[5]*regs[2]+(6010/regs[2])) < regs[1] && regs[3] == 0
  optimize_600 = regs[ip_index] == 10 && (regs[5]*regs[2]+(610/regs[2])) < regs[1] && regs[3] == 0
  optimize_125 = regs[ip_index] == 10  \
    && ( \
      (regs[5]*regs[2]+(135/regs[2])) < regs[1]  \
      || (regs[5] * regs[2] > regs[1] && regs[5] < regs[1]) \
    ) && regs[3] == 0
  optimize_25 = regs[ip_index] == 10 && (regs[5]*regs[2]+(35/regs[2])) < regs[1] && regs[3] == 0
  optimize = regs[ip_index] == 10 && (regs[5]*regs[2]+(5/regs[2])) < regs[1] && regs[3] == 0

  another_optimize = regs[ip_index] == 10 && regs[3] == 1 && regs[2] < regs[1]

  if optimize_8000000
    data[:regs][5] += 8000000
    return data
  elsif optimize_800000
    data[:regs][5] += 800000
    return data
  elsif optimize_70000
    data[:regs][5] += 70000
    return data
  elsif optimize_6000
    data[:regs][5] += 6000
    return data
  elsif optimize_600
    data[:regs][5] += 600
    return data
  elsif optimize_125
    data[:regs][5] += 125
    return data
  elsif optimize_25
    data[:regs][5] += 25
    return data
  elsif optimize
    data[:regs][5] += 1
    return data
  else
    cpu = Compute.new
    new_regs = cpu.public_send(op, regs, a, b, c)
    #print "ip=#{regs[ip_index]} #{regs} -> #{op} #{a} #{b} #{c} -> #{new_regs} -> "
    new_regs[ip_index] += 1
    #puts "#{new_regs}"
  end


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

filename = 'input.txt'
data = parse_file(filename)
loop do
  data = tick(data)
  break if invalid_ip(data)
  #STDIN.getch
end
puts data
puts data[:regs][0]

# That's not the right answer; your answer is too low. If you're stuck, there
# are some general tips on the about page, or you can ask for hints on the
# subreddit. Please wait one minute before trying again. (You guessed 10551312.)

