#!/usr/bin/env ruby
x = y = y2 = aim = 0
ARGF.each do |line|
  x += Integer($1) and y2 += aim * Integer($1) if line =~ /forward (\d+)/
  y += Integer($1) and aim += Integer($1)      if line =~ /down (\d+)/
  y -= Integer($1) and aim -= Integer($1)      if line =~ /up (\d+)/
end
puts x * y
puts x * y2
