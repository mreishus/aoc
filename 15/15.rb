#!/usr/bin/env ruby

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

require 'pp'

def tests
  raise 'fail' unless true == true
end

def readfile(filename)
  max_x, max_y = readfile_coords(filename)
  grid = Array.new(max_x+1) { Array.new(max_y + 1)}
  units = []
  unit_id = 0
  y = 0
  File.readlines(filename).each do |line|
    x = 0
    line.chars.each do |c|
      if c == '#'
        grid[x][y] = '#'
      elsif c == 'G'
        grid[x][y] = '.'
        unit = {x: x, y: y, type: 'gob', display: 'G', id: unit_id, hp: 200, atk: 3}
        unit_id += 1
        units.push unit
      elsif c == 'E'
        grid[x][y] = '.'
        unit = {x: x, y: y, type: 'elf', display: 'E', id: unit_id, hp: 200, atk: 3}
        unit_id += 1
        units.push unit
      elsif c == '.'
        grid[x][y] = '.'
      end
      x += 1
    end
    y += 1
  end
  {grid: grid, units: units, max_x: max_x, max_y: max_y}
end

# Gets max_x and max_y, 0 indexed, from file
def readfile_coords(filename)
  max_x = 0
  max_y = 0
  y = 0
  File.readlines(filename).each do |line|
    line = line.strip
    max_x = [max_x, line.length].max
    y += 1
  end
  max_y = y
  [max_x, max_y]
end

def display(gamedata)
  grid, units, max_x, max_y = gamedata.values_at(:grid, :units, :max_x, :max_y)

  0.upto(max_y) do |y|
    0.upto(max_x) do |x|
      #puts "x [#{x}]"
      unit = units.find{ |u| x.to_i == u[:x] && y.to_i == u[:y] }
      print unit == nil ? grid[x][y] : unit[:display]
    end
    print "\n"
  end
end

def tick(input_gamedata)
  gamedata = input_gamedata.dup
  units = gamedata[:units]
  turn_order = units.sort_by { |h| [h[:y].to_i, h[:x].to_i] }.map { |u| u[:id] }
  turn_order.each do |id|
    gamedata = tick_unit(gamedata, id)
  end
  gamedata
end

def collapse(x, y)
  x.to_s + '_' + y.to_s
end

def expand(xystring)
  xystring.split('_').map(&:to_i)
end

def tick_unit(input_gamedata, id)
  gamedata = input_gamedata.dup
  grid, units = gamedata.values_at(:grid, :units)
  unit = units.find { |u| u[:id] == id }

  # how many enemies?
  enemies = units.reject { |u| u[:type] == unit[:type] }
  return gamedata if enemies.count.zero?

  # squares in range
  in_range = enemies.map do |u|
      [
        { x: u[:x]+1, y: u[:y], reachable: nil, range: nil },
        { x: u[:x]-1, y: u[:y], reachable: nil, range: nil },
        { x: u[:x], y: u[:y]+1, reachable: nil, range: nil },
        { x: u[:x], y: u[:y]-1, reachable: nil, range: nil },
      ]
    end
    .flatten!
    .uniq
    .reject { |coord| grid[coord[:x]][coord[:y]] == '#' }

  problem = {grid: grid, units: units, unit: unit, targets: in_range}
  z = bfs(problem)
  action = z.first

  pp z
  if action == "right"
    unit[:x] += 1
  elsif action == "left"
    unit[:x] -= 1
  elsif action == "up"
    unit[:y] -= 1
  elsif action == "down"
    unit[:y] += 1
  end

  # move
  #unit[:x] += 1

  # return
  gamedata
end

def bfs(problem)
  grid, unit, targets = problem.values_at(:grid, :unit, :targets)

  open_set = [collapse(unit[:x], unit[:y])]
  closed_set = []
  meta = {}

  while open_set.count > 0
    subtree_root = open_set.pop
    str_x, str_y = expand(subtree_root)

    if is_goal(problem, subtree_root)
      return construct_path(subtree_root, meta)
    end

    get_possible_steps(problem, subtree_root).each do |step|
      child, action = step.values_at(:child, :action)
      next if closed_set.include? child

      meta[child] = [subtree_root, action]
      open_set.push(child)
    end

    closed_set.push(subtree_root)
  end
end

def construct_path(node, meta)
  actions = []

  while meta[node] != nil
    node, action = meta[node]
    actions.push(action)
  end
  actions
end

def is_goal(problem, subtree_root)
  x, y = expand(subtree_root)
  targets = problem[:targets]
  targets.find {|t| t[:x] == x && t[:y] == y } != nil
end

def get_possible_steps(problem, subtree_root)
  grid, units = problem.values_at(:grid, :units)
  x, y = expand(subtree_root)
  steps = []
  if (is_ok(x+1, y, grid, units))
    steps.push({child: collapse(x+1, y), action: 'right'})
  end
  if (is_ok(x-1, y, grid, units))
    steps.push({child: collapse(x-1, y), action: 'left'})
  end
  if (is_ok(x, y+1, grid, units))
    steps.push({child: collapse(x, y+1), action: 'down'})
  end
  if (is_ok(x, y-1, grid, units))
    steps.push({child: collapse(x, y-1), action: 'up'})
  end
  steps
end

def is_ok(x, y, grid, units)
  if grid[x] == nil || grid[x][y] == nil || grid[x][y] == '#'
    return false
  end

  unit = units.find { |u| u[:x] == x && u[:y] == y }
  unit.nil?
end

def part1(filename)
  gamedata = readfile(filename)
  display(gamedata)
  gamedata = tick(gamedata)
  display(gamedata)
  #gamedata = tick(gamedata)
  #display(gamedata)
  #gamedata = tick(gamedata)
  #display(gamedata)
end

begin_tests = Time.now
tests()
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

["input_small.txt"].each do |x|
  puts "Part 1, target: #{x}"
  part1(x)
end
