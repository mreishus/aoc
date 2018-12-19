#!/usr/bin/env ruby

require 'pp'
require 'duplicate'

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

def tests
  test_input_small
end

def test_input_small
  filename = 'input_small.txt'
  gamedata = readfile(filename)
  board_init = display_string(gamedata)

  gamedata = tick(gamedata)
  board_p1 = display_string(gamedata)
  gamedata = tick(gamedata)
  board_p2 = display_string(gamedata)
  gamedata = tick(gamedata)
  board_p3 = display_string(gamedata)
  gamedata = tick(gamedata)
  board_p4 = display_string(gamedata)

  p1_expect = %(
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.
)
  p1_expect[0] = ''
	p2_expect = %(
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||
)
  p2_expect[0] = ''
	p3_expect = %(
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||
)
  p3_expect[0] = ''
	p4_expect = %(
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||
)
  p4_expect[0] = ''
	
  raise 'fail 1 small' unless p1_expect == board_p1
  raise 'fail 2 small' unless p2_expect == board_p2
  raise 'fail 3 small' unless p3_expect == board_p3
  raise 'fail 4 small' unless p4_expect == board_p4
end

# INPUT: filename(text)
# OUTPUT: gamedata hash(grid(2d array), units(array of hashes), max_x(int), max_y(int))
# Parses the file into the main data.
def readfile(filename)
  max_x, max_y = readfile_coords(filename)
  grid = Array.new(max_x) { Array.new(max_y) }
  y = 0
  File.readlines(filename).each do |line|
    x = 0
    line.strip.chars.each do |c|
      grid[x][y] = c
      x += 1
    end
    y += 1
  end
  { grid: grid, max_x: max_x, max_y: max_y }
end

# INPUT: filename(text)
# OUTPUT: [max_x, max_y]  both integers
# Gets max_x and max_y, 0 indexed, from file. Grid size
def readfile_coords(filename)
  max_x = 0
  y = 0
  File.readlines(filename).each do |line|
    line = line.strip
    max_x = [max_x, line.length].max
    y += 1
  end
  max_y = y
  [max_x, max_y]
end

# INPUT: gamedata
# OUTPUT: Prints board to screen
def display(gamedata)
  puts ''
  print display_string(gamedata)
end

# INPUT: gamedata
# OUTPUT: Prints board to string
def display_string(gamedata)
  grid, max_x, max_y = gamedata.values_at(:grid, :max_x, :max_y)
  output = ''

  0.upto(max_y - 1) do |y|
    0.upto(max_x - 1) do |x|
      output += grid[x][y]
    end
    output += "\n"
  end
  output
end

=begin
An open acre . will become filled with trees | if three or more adjacent acres contained trees. Otherwise, nothing happens.
An acre filled with trees | will become a lumberyard # if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
An acre containing a lumberyard # will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
=end


def tick(gamedata_in)
  gamedata_out = Duplicate.duplicate(gamedata_in)
  max_x, max_y = gamedata_in.values_at(:max_x, :max_y)

  0.upto(max_y - 1) do |y|
    0.upto(max_x - 1) do |x|
      square = gamedata_in[:grid][x][y]
      if square == '.'
        if three_or_more_neighbors(gamedata_in, x, y, '|')
          gamedata_out[:grid][x][y] = '|'
        end
      elsif square == '|'
        if three_or_more_neighbors(gamedata_in, x, y, '#')
          gamedata_out[:grid][x][y] = '#'
        end
      elsif square == '#'
        if !one_or_more_neighbors(gamedata_in, x, y, '#') || !one_or_more_neighbors(gamedata_in, x, y, '|')
          gamedata_out[:grid][x][y] = '.'
        end
      end
    end
  end

  gamedata_out
end

def safe_check(gamedata, x, y)
  grid, max_x, max_y = gamedata.values_at(:grid, :max_x, :max_y)
  return nil if x >= max_x || y >= max_y || x < 0 || y < 0

  grid[x][y]
end

def three_or_more_neighbors(gamedata, x, y, target)
  n_or_more_neighbors(gamedata, x, y, 3, target)
end

def one_or_more_neighbors(gamedata, x, y, target)
  n_or_more_neighbors(gamedata, x, y, 1, target)
end

# Looking inside gamedata, at point x, y,
# To see if n or more neighbors match target
def n_or_more_neighbors(gamedata, x, y, n, target)
  neighbor_count = 0
  -1.upto(1).each do |dy|
    -1.upto(1).each do |dx|
      next if dx.zero? && dy.zero?

      neighbor_count += 1 if safe_check(gamedata, x+dx, y+dy) == target
      return true if neighbor_count >= n
    end
  end
  false
end



############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

filename = 'input_small.txt'
gamedata = readfile(filename)
display(gamedata)

gamedata = tick(gamedata)
display(gamedata)
