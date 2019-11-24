#!/usr/bin/env ruby
require 'require_all'
require_all './lib'

text = File.read('../input.txt').chomp
puts 'Part1: '
puts Day01.part1(text)
puts 'Part2: '
puts Day01.part2(text)
