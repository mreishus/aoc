#!/usr/bin/env ruby

require 'pp'

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

def tests
  depth = 510
  raise 'ind01' unless Grid.geoind( Complex(0, 0), Complex(10, 10), depth ) == 0
  raise 'ind01' unless Grid.geoind( Complex(10, 10), Complex(10, 10), depth ) == 0

  raise 'f1' unless Grid.geoind( Complex(1, 0), Complex(10, 10), depth ) == 16807
  raise 'f2' unless Grid.erosionlevel( Complex(1, 0), Complex(10, 10), depth ) == 17317
  raise 'f3' unless Grid.type( Complex(1, 0), Complex(10, 10), depth ) == 1

  raise 'f4' unless Grid.geoind( Complex(0, 1), Complex(10, 10), depth ) == 48271
  raise 'f5' unless Grid.erosionlevel( Complex(0, 1), Complex(10, 10), depth ) == 8415
  raise 'f6' unless Grid.type( Complex(0, 1), Complex(10, 10), depth ) == 0

  raise 'f7' unless Grid.geoind( Complex(1, 1), Complex(10, 10), depth ) == 145722555
  raise 'f8' unless Grid.erosionlevel( Complex(1, 1), Complex(10, 10), depth ) == 1805
  raise 'f9' unless Grid.type( Complex(1, 1), Complex(10, 10), depth ) == 2

  raise 'f10' unless Grid.geoind( Complex(10, 10), Complex(10, 10), depth ) == 0
  raise 'f11' unless Grid.erosionlevel( Complex(10, 10), Complex(10, 10), depth ) == 510
  raise 'f12' unless Grid.type( Complex(10, 10), Complex(10, 10), depth ) == 0

  raise 'f13' unless Grid.total_risk(Complex(10, 10), depth) == 114
end

class Grid
  def self.total_risk(targetcoord, depth)
    tx, ty = [targetcoord.real, targetcoord.imag]
    risk = 0
    0.upto(tx) do |x|
      0.upto(ty) do |y|
        risk += Grid.type( Complex(x, y), targetcoord, depth)
      end
    end
    risk
  end

  def self.geoind(coord, targetcoord, depth)
    x, y = [coord.real, coord.imag]
    tx, ty = [targetcoord.real, targetcoord.imag]
    return 0 if (x == 0 && y == 0) || (x == tx && y == ty)
    return x * 16807 if y.zero?
    return y * 48271 if x.zero?

    Grid.erosionlevel(Complex(x - 1, y), targetcoord, depth) * Grid.erosionlevel(Complex(x, y - 1), targetcoord, depth)
  end

  def self.erosionlevel(coord, targetcoord, depth)
    (Grid.geoind(coord, targetcoord, depth) + depth) % 20183
  end

  def self.type(coord, targetcoord, depth)
    Grid.erosionlevel(coord, targetcoord, depth) % 3
  end
end


############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

target = Complex(10, 10)
