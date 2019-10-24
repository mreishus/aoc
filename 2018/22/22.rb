#!/usr/bin/env ruby

require 'pp'
require 'priority_queue'
# sudo gem install PriorityQueue
# https://github.com/supertinou/priority-queue

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
  raise 'f14' unless Grid.total_risk(Complex(11, 718), 11739) == 8735
  test_part2
end

def test_part2
  initial = Complex(0, 0)
  target = Complex(10, 10)
  depth = 510

  initial_pair = [initial, 2] # Torch
  target_pair = [target, 2] # Torch
  raise 'p2' unless part2(initial_pair, target_pair, depth) == 45
end

class Grid
  def self.total_risk(targetcoord, depth)
    tx, ty = [targetcoord.real, targetcoord.imag]
    risk = 0
    0.upto(tx) do |x|
      0.upto(ty) do |y|
        risk += Grid.type(Complex(x, y), targetcoord, depth)
      end
    end
    risk
  end

  def self.geoind(coord, targetcoord, depth)
    @grid_calculations ||= Hash.new do |h, key|
      coord = key[0]
      targetcoord = key[1]
      depth = key[2]

      x, y = [coord.real, coord.imag]
      tx, ty = [targetcoord.real, targetcoord.imag]
      answer = nil
      if (x.zero? && y.zero?) || (x == tx && y == ty)
        answer = 0
      elsif y.zero?
        answer = x * 16807
      elsif x.zero?
        answer = y * 48271
      else
        answer = Grid.erosionlevel(Complex(x - 1, y), targetcoord, depth) * Grid.erosionlevel(Complex(x, y - 1), targetcoord, depth)
      end
      h[key] = answer
    end
    @grid_calculations[[coord, targetcoord, depth]]
  end

  def self.erosionlevel(coord, targetcoord, depth)
    (Grid.geoind(coord, targetcoord, depth) + depth) % 20183
  end

  def self.type(coord, targetcoord, depth)
    @type_calculations ||= Hash.new do |h, key|
      coord = key[0]
      targetcoord = key[1]
      depth = key[2]

      answer = Grid.erosionlevel(coord, targetcoord, depth) % 3
      h[key] = answer
    end
    @type_calculations[[coord, targetcoord, depth]]
  end
end

# tools = none(0) | climb(1) | torch(2)
# types:
#   0=rocky    climb or torch
#   1=wet      climb or none
#   2=narrow   torch or none

def tool_valid(coord, target, depth, tool)
  type = Grid.type(coord, target, depth)
  return [1, 2].include? tool if type.zero?
  return [0, 1].include? tool if type == 1
  return [0, 2].include? tool if type == 2

  false
end

$DIRECTIONS = [Complex(1, 0), Complex(-1, 0), Complex(0, 1), Complex(0, -1)]

def valid_moves(coord_tool_pair, target_tool_pair, depth)
  coord, tool = coord_tool_pair
  target, = target_tool_pair

  moves = []
  # Option 1: Moving with the current tool
  $DIRECTIONS.each do |direction|
    destination = coord + direction
    dx, dy = [destination.real, destination.imag]
    next if dx < 0 || dy < 0 || !tool_valid(destination, target, depth, tool)

    moves.push({coord_tool_pair: [destination, tool], cost: 1})
  end

  # Option 2: Changing the current tool
  [0, 1, 2].each do |newtool|
    next if newtool == tool || !tool_valid(coord, target, depth, newtool)

    moves.push({coord_tool_pair: [coord, newtool], cost: 7})
  end
  moves
end

def heuristic(coord_tool_pair, target_tool_pair)
  coord, begin_tool = coord_tool_pair
  target, end_tool  = target_tool_pair

  sx, sy = [coord.real, coord.imag]
  dx, dy = [target.real, target.imag]

  mdist = (sx - dx).abs + (sy - dy).abs
  return mdist + 7 if mdist <= 15 && begin_tool != end_tool

  mdist
end

def reconstruct_path(came_from, current)
  total_path = [current]
  while came_from.key? current
    current = came_from[current]
    total_path.push current
  end
  total_path
end

def astar(initial, goal, depth)
  closed_set = {}
  came_from = {}

  # Cost of initial -> This node
  travel_score = Hash.new(999999999999)
  travel_score[initial] = 0

  # Cost of Initial -> This node -> destination, using a heuristic for what we haven't figured out yet
  est_full_travel_score = Hash.new(999999999999)
  est_full_travel_score[initial] = heuristic(initial, goal)

  open_set = PriorityQueue.new
  open_set.push initial, est_full_travel_score[initial]

  loop do
    current = open_set.delete_min_return_key
    return reconstruct_path(came_from, current) if current == goal

    closed_set[current] = 1

    moves = valid_moves(current, goal, depth)
    moves.each do |move_struct|
      move, cost = [move_struct[:coord_tool_pair], move_struct[:cost]]
      next if closed_set.key? move

      tenative_travel_score = travel_score[current] + cost
      if !open_set.has_key? move
        open_set.push move, 99999999
      elsif tenative_travel_score >= travel_score[move]
        next
      end

      came_from[move] = current
      travel_score[move] = tenative_travel_score
      est_full_travel_score[move] = travel_score[move] + heuristic(move, goal)
      open_set.change_priority move, est_full_travel_score[move]
    end
  end
end

def calculate_time(path)
  last_seen = nil
  time = 0
  path.each do |item|
    if last_seen.nil?
      last_seen = item
      next
    end

    this_coord, this_tool = item
    last_coord, last_tool = last_seen

    if last_tool != this_tool
      time += 7
    else
      time += 1
    end
    last_seen = item
  end
  time
end

def part2(initial_pair, target_pair, depth)
  begin_pathfind = Time.now
  path = astar(initial_pair, target_pair, depth)
  end_pathfind = Time.now
  puts "AStar Time - #{end_pathfind.to_ms - begin_pathfind.to_ms}ms"

  calculate_time(path)
end


############## MAIN #####################

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

depth = 11_739
target = Complex(11, 718)
puts 'Part1: Risk is '
puts Grid.total_risk(target, depth)

## Part 2:
initial = Complex(0, 0)
initial_pair = [initial, 2] # Torch
target_pair = [target, 2] # Torch
time = part2(initial_pair, target_pair, depth)
puts 'Part2: Time is'
puts time
