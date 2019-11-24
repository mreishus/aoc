#!/usr/bin/env ruby
require 'require_all'
require_all './lib'

text = File.read('../input.txt').chomp
puts Day01.part1(text)
