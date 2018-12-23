#!/usr/bin/env ruby

require 'pp'

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

class NanoBot
  attr_accessor :x, :y, :z, :r
  def initialize(x, y, z, r)
    @x, @y, @z, @r = x, y, z, r
  end

  def dist(bot2)
    (@x - bot2.x).abs + (@y - bot2.y).abs + (@z - bot2.z).abs
  end

  def has_target_in_range(bot2)
    self.dist(bot2) <= @r
  end
end

def parse_file(filename)
  bots = []
  File.readlines(filename).each do |line|
    x, y, z, r = line.strip.match(/pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)/).captures.map(&:to_i)
    bots.push(NanoBot.new(x, y, z, r))
  end
  bots
end

def tests
  a = NanoBot.new(1, 2, 3, 10)
  b = NanoBot.new(2, 3, 5, 10)
  raise 'x' unless a.x == 1
  raise 'y' unless a.y == 2
  raise 'z' unless a.z == 3
  raise 'r' unless a.r == 10
  raise 'dist1' unless a.dist(b) == 4
  raise 'dist2' unless b.dist(a) == 4

  bot1 = NanoBot.new(0, 0, 0, 4)
  bot2 = NanoBot.new(1, 0, 0, 1)
  bot3 = NanoBot.new(4, 0, 0, 3)
  bot4 = NanoBot.new(0, 2, 0, 1)
  bot5 = NanoBot.new(0, 5, 0, 3)
  raise 'in_range 2' unless bot1.has_target_in_range(bot2)
  raise 'in_range 3' unless bot1.has_target_in_range(bot3)
  raise 'in_range 4' unless bot1.has_target_in_range(bot4)
  raise 'in_range 5' unless !bot1.has_target_in_range(bot5)

  raise 'in range' unless part1('input_small.txt') == 7
end

def part1(filename)
  bots = parse_file(filename)
  strongest = bots.max_by(&:r)
  bots.select { |bot| strongest.has_target_in_range(bot) }.count
end

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

puts 'Part1: '
pp part1('input.txt')
