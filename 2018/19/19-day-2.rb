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
  end

  def addi(r, a, b, c)
    r[c] = r[a] + b
  end

  def mulr(r, a, b, c)
    r[c] = r[a] * r[b]
  end

  def muli(r, a, b, c)
    r[c] = r[a] * b
  end

  def banr(r, a, b, c)
    r[c] = r[a] & r[b]
  end

  def bani(r, a, b, c)
    r[c] = r[a] & b
  end

  def borr(r, a, b, c)
    r[c] = r[a] | r[b]
  end

  def bori(r, a, b, c)
    r[c] = r[a] | b
  end

  def setr(r, a, _b, c)
    r[c] = r[a]
  end

  def seti(r, a, _b, c)
    r[c] = a
  end

  def gtir(r, a, b, c)
    r[c] = a > r[b] ? 1 : 0
  end

  def gtri(r, a, b, c)
    r[c] = r[a] > b ? 1 : 0
  end

  def gtrr(r, a, b, c)
    r[c] = r[a] > r[b] ? 1 : 0
  end

  def eqir(r, a, b, c)
    r[c] = a == r[b] ? 1 : 0
  end

  def eqri(r, a, b, c)
    r[c] = r[a] == b ? 1 : 0
  end

  def eqrr(r, a, b, c)
    r[c] = r[a] == r[b] ? 1 : 0
  end

  def all_instructions
    %w[
      addr
      addi
      mulr
      muli
      banr
      bani
      borr
      bori
      setr
      seti
      gtir
      gtri
      gtrr
      eqir
      eqri
      eqrr
    ]
  end
end

$cpu = Compute.new

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
  exe = data[:program][data[:regs][data[:ip_index]]]

  #print "ip=#{data[:regs][data[:ip_index]]} #{data[:regs]} "
  if data[:regs][data[:ip_index]] == 3
    ##pp data[:regs]
    r = data[:regs]
    r[0] += r[2] if r[1] % r[2] == 0
    r[5] = r[1] + 1
    r[3] = 1
    data[:regs][data[:ip_index]] = 12
    ##pp data[:regs]
    return data
  end

  $cpu.send(exe[:op], data[:regs], exe[:a], exe[:b], exe[:c])

  #print "-> #{exe[:op]} #{exe[:a]} #{exe[:b]} #{exe[:c]} -> #{data[:regs]} -> "
  data[:regs][data[:ip_index]] += 1

  #puts "#{data[:regs]}"

  data
end

def invalid_ip(data)
  data[:program][data[:regs][data[:ip_index]]].nil?
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
i = 0
loop do
  tick(data)

  #if i % 100000 == 0
  #  i = 0
  #  pp data[:regs]
  #end

  #puts data
  break if invalid_ip(data)
  #STDIN.getch
  i += 1
end
puts data
puts data[:regs][0]

# That's not the right answer; your answer is too low. If you're stuck, there
# are some general tips on the about page, or you can ask for hints on the
# subreddit. Please wait one minute before trying again. (You guessed 10551312.)
