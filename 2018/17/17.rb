#!/usr/bin/env ruby

require 'pp'

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

def tests
  end_to_end_small
  end_to_end_large
end

def end_to_end_small
  p1, p2 = filename_to_p1_p2('input_small.txt')
  raise 'small p1 failed' unless p1 == 57
  raise 'small p2 failed' unless p2 == 29
end

def end_to_end_large
  p1, p2 = filename_to_p1_p2('input.txt')
  raise 'large p1 failed' unless p1 == 44_743
  raise 'large p2 failed' unless p2 == 34_172
end

def filename_to_p1_p2(filename)
  simdata = add_spring(parse_file(filename))
  simdata = waterflow(simdata, 500, 0)
  part1 = count_part_1(simdata)
  part2 = count_part_2(simdata)
  [part1, part2]
end

def init_grid(grid_max_x, grid_max_y)
  grid = Array.new(grid_max_x + 1) { Array.new(grid_max_y + 1) }
  0.upto(grid_max_y) { |y| 0.upto(grid_max_x) { |x| grid[x][y] = '.' } }
  grid
end

def update_maxmins(mm, x, y)
  mm[:min_x] = x if mm[:min_x].nil? || x < mm[:min_x]
  mm[:max_x] = x if mm[:max_x].nil? || x > mm[:max_x]
  mm[:min_y] = y if mm[:min_y].nil? || y < mm[:min_y]
  mm[:max_y] = y if mm[:max_y].nil? || y > mm[:max_y]
  mm
end

def parse_file(filename)
  # Could scan input file for max
  grid = init_grid(1_850, 1_850)

  maxmins = {}

  File.readlines(filename).each do |line|
    if line =~ /^x/
      x, y1, _, y2 =
        line.strip.match(/x=(\d+), y=(\d+)(..(\d+))?/).captures.map(&:to_i)
      if y2.zero?
        grid[x][y1] = '#'
      else
        (y1..y2).each { |y| grid[x][y] = '#' }
        maxmins = update_maxmins(maxmins, x, y2)
      end
      maxmins = update_maxmins(maxmins, x, y1)
    elsif line =~ /^y/
      y, x1, _, x2 =
        line.strip.match(/y=(\d+), x=(\d+)(..(\d+))?/).captures.map(&:to_i)
      if x2.zero?
        grid[x1][y] = '#'
      else
        (x1..x2).each { |x| grid[x][y] = '#' }
        maxmins = update_maxmins(maxmins, x2, y)
      end
      maxmins = update_maxmins(maxmins, x1, y)
    end
  end

  { grid: grid, maxmins: maxmins }
end

def add_spring(simdata)
  grid, maxmins = simdata.values_at(:grid, :maxmins)
  spring_x = 500
  spring_y = 0
  grid[spring_x][spring_y] = '+'
  { grid: grid, maxmins: maxmins }
end

# INPUT: simdata
# OUTPUT: Prints board to screen
def display(simdata)
  puts ''
  display_no_buffer(simdata)
  # print display_string(simdata)
end

def display_no_buffer(simdata)
  max_x, max_y, min_x, min_y =
    simdata[:maxmins].values_at(:max_x, :max_y, :min_x, :min_y)

  min_y.upto(max_y) do |y|
    (min_x - 1).upto(max_x + 1) { |x| print simdata[:grid][x][y] }
    print "\n"
  end
end

# INPUT: simdata
# OUTPUT: Prints board to string
def display_string(simdata)
  max_x, max_y, min_x, min_y =
    simdata[:maxmins].values_at(:max_x, :max_y, :min_x, :min_y)
  output = ''

  min_y.upto(max_y + 25) do |y|
    (min_x - 1).upto(max_x + 1 + 25) { |x| output += simdata[:grid][x][y] }
    output += "\n"
  end
  output
end

def collapse(x, y)
  x.to_s + '_' + y.to_s
end

def expand(xystring)
  xystring.split('_').map(&:to_i)
end

def waterflow(simdata, spout_x, spout_y)
  grid, maxmins = simdata.values_at(:grid, :maxmins)

  grid[spout_x][spout_y + 1] = '|'
  process_me = [collapse(spout_x, spout_y + 1)]

  until process_me.empty?
    x, y = expand(process_me.shift)
    next if y > maxmins[:max_y]

    square = grid[x][y]
    next if square == '#'

    if square == '~'
      if %w[. |].include? grid[x + 1][y]
        grid[x + 1][y] = '~'
        add_to_queue!(process_me, x + 1, y)
      end
      if %w[. |].include? grid[x - 1][y]
        grid[x - 1][y] = '~'
        add_to_queue!(process_me, x - 1, y)
      end
    end

    next unless square == '|'

    # From here below.. working on '|'
    # Flows down if below is clear
    if grid[x][y + 1] == '.'
      grid[x][y + 1] = '|'
      add_to_queue!(process_me, x, y + 1)
    end

    # Flows left/right if bottom is hard
    bottom_hard = %w[~ #].include? grid[x][y + 1]
    if grid[x + 1][y] == '.' && bottom_hard
      grid[x + 1][y] = '|'
      add_to_queue!(process_me, x + 1, y)
    end
    if grid[x - 1][y] == '.' && bottom_hard
      grid[x - 1][y] = '|'
      add_to_queue!(process_me, x - 1, y)
    end

    # Hardens (becomes ~) if underneath is ~ or # as we go left/right until we hit a wall
    still_water = true
    # Left..
    dx = -1
    loop do
      break if grid[x + dx][y] == '#'

      unless %w[~ #].include? grid[x + dx][y + 1]
        still_water = false
        break
      end
      dx -= 1
    end

    # Right..
    dx = 1
    loop do
      break if grid[x + dx][y] == '#'

      unless %w[~ #].include? grid[x + dx][y + 1]
        still_water = false
        break
      end
      dx += 1
    end

    if still_water
      grid[x][y] = '~'
      add_to_queue!(process_me, x, y)
    end
  end
  { grid: grid, maxmins: maxmins }
end

def add_to_queue!(process_me, x, y)
  process_me.push(collapse(x, y))
  process_me.push(collapse(x, y - 1))
  # Everything works without these...
  # process_me.push(collapse(x+1, y))
  # process_me.push(collapse(x-1, y))
  # process_me.push(collapse(x, y+1))
end

def count_part_1(simdata)
  count(simdata, %w[~ |])
end

def count_part_2(simdata)
  count(simdata, %w[~])
end

def count(simdata, valids)
  grid, maxmins = simdata.values_at(:grid, :maxmins)
  max_x, max_y, min_x, min_y =
    simdata[:maxmins].values_at(:max_x, :max_y, :min_x, :min_y)

  total_water = 0

  min_y.upto(max_y) do |y|
    (min_x - 10).upto(max_x + 10) do |x|
      square = grid[x][y]
      total_water += 1 if valids.include? square
    end
  end

  total_water
end

############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

p1, p2 = filename_to_p1_p2('input_small.txt')
puts "Part1: #{p1}"
puts "Part2: #{p2}"
