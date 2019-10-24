#!/usr/bin/env ruby

require 'pp'

class Star
  attr_accessor :id, :w, :x, :y, :z, :avg
  def initialize(id, w, x, y, z)
    @id = id
    @w = w
    @x = x
    @y = y
    @z = z

    @avg = (w.to_f + x.to_f + y.to_f + z.to_f) / 4.to_f
  end

  def dist(star2)
    (@w - star2.w).abs + (@x - star2.x).abs + (@y - star2.y).abs + (@z - star2.z).abs
  end
end

$MAX_CONST_ID = 0
class Constellation
  attr_accessor :stars, :id
  def initialize(stars)
    @id = $MAX_CONST_ID
    $MAX_CONST_ID += 1
    @stars = stars
  end

  def has_any_w(w)
    @stars.any?{ |s| s.w == w }
  end
  def has_any_x(x)
    @stars.any?{ |s| s.x == x }
  end
  def has_any_y(y)
    @stars.any?{ |s| s.y == y }
  end
  def has_any_z(z)
    @stars.any?{ |s| s.z == z }
  end
  def is_possible_match(star)
    has_any_w(star.w) || has_any_x(star.x) || has_any_y(star.y) || has_any_z(star.z)
  end
  def is_actual_match(star)
    @stars.any?{ |s| s.dist(star) <= 3 }
  end
end

def parse_file(filename)
  stars = []
  id = 0
  File.readlines(filename).each do |line|
    main_re = /(-?\d+),(-?\d+),(-?\d+),(-?\d+)/
    w, x, y, z = line.strip.match(main_re).captures.map(&:to_i)
    stars.push Star.new(id, w, x, y, z)
    id += 1
  end
  stars
end

def find_constellation(star, constellations)
  #puts "Looking for star #{star.id}"
  matches = []
  constellations.each do |const|
    #next unless const.is_possible_match(star) && const.is_actual_match(star)
    matches.push(const) if const.is_actual_match(star)
  end

  if matches.nil? || matches.empty?
    #puts "Unable to find match for #{star.id}"
    return [nil, 'none']
  elsif matches.count == 1
    return [matches, 'single']
  else 
    return [matches, 'multiple']
  end
end

def part1(filename)
  stars = parse_file(filename)
  constellations = []

  stars.sort_by {|s| s.avg}.each do |star|
    matches, match_type = find_constellation(star, constellations)
    if match_type == 'none'
      new_const = Constellation.new([star])
      constellations.push(new_const)
    elsif match_type == 'single'
      matches.first.stars.push(star)
    else
      # Multiple matches, we need to merge constellations
      parent = matches.shift
      parent.stars.push(star)

      ids_to_delete = []
      matches.each do |merge_const|
        ids_to_delete.push(merge_const.id)
        merge_const.stars.each do |star|
          parent.stars.push(star)
        end
      end
      constellations.reject! { |y| ids_to_delete.include? y.id }

    end
  end
  #pp constellations
  constellations.count
end

raise 'p1 1' unless part1('input_small1.txt') == 2
raise 'p1 2' unless part1('input_small2.txt') == 4
raise 'p1 3' unless part1('input_small3.txt') == 3
raise 'p1 4' unless part1('input_small4.txt') == 8
puts 'All tests passed'

puts 'Part1:'
puts part1('input.txt')
