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
        { x: u[:x]+1, y: u[:y], reachable: nil, range: nil, paths: [] },
        { x: u[:x]-1, y: u[:y], reachable: nil, range: nil, paths: [] },
        { x: u[:x], y: u[:y]+1, reachable: nil, range: nil, paths: [] },
        { x: u[:x], y: u[:y]-1, reachable: nil, range: nil, paths: [] },
      ]
    end
    .flatten!
    .uniq
    .reject { |coord| grid[coord[:x]][coord[:y]] == '#' }

  already_in_range = in_range.find { |t| t[:x] == unit[:x] && t[:y] == unit[:y] } != nil
  return gamedata if already_in_range

  problem = {grid: grid, units: units, unit: unit, targets: in_range}
  bfs(problem)

  ## Now we have to find the appropriate target
  move_to = problem[:targets]
    .select { |t| !t[:range].nil? }
    .sort_by{ |t| t[:range] }

  return gamedata if move_to.empty? # Found no reachable targets

  shortest_range = move_to.first[:range]
  move_to = move_to
    .select{ |t| t[:range] == shortest_range }     # Nearest only
    .sort_by{ |t| [t[:y], t[:x]] }                 # Reading order
    .first
  #pp move_to
  paths = move_to[:paths]

  if paths.select{ |p| p.first == "up"}.any?
    unit[:y] -= 1
  elsif paths.select{ |p| p.first == "left"}.any?
    unit[:x] -= 1
  elsif paths.select{ |p| p.first == "right"}.any?
    unit[:x] += 1
  elsif paths.select{ |p| p.first == "down"}.any?
    unit[:y] += 1
  end

  # return
  gamedata
end

def bfs(problem)
  unit, targets = problem.values_at(:unit, :targets)

  open_set = [collapse(unit[:x], unit[:y])]
  closed_set = []
  meta = {}
  min_range = nil

  while open_set.count > 0
    subtree_root = open_set.pop

    if is_goal(problem, subtree_root)
      path = construct_path(subtree_root, meta)
      range = path.length
      node_x, node_y = expand(subtree_root)
      t = targets.find { |tg| tg[:x] == node_x && tg[:y] == node_y }
      t[:paths].push path unless t[:paths].include? path
      t[:range] = range if t[:range].nil? || t[:range] > range
      min_range = range if min_range.nil? || range < min_range
      t[:reachable] = true
      # puts "Writing range #{t[:range]}"
      return if range > min_range # return early, we have already seen all the shortest paths..
    end

    get_possible_steps(problem, subtree_root).each do |step|
      child, action = step.values_at(:child, :action)
      next if closed_set.include? child

      meta[child] = [subtree_root, action]
      open_set.unshift(child)
    end

    closed_set.push(subtree_root)
  end
end

def construct_path(node, meta)
  actions = []

  while !meta[node].nil?
    node, action = meta[node]
    actions.push(action)
  end
  actions.reverse
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
  if is_ok(x, y+1, grid, units)
    steps.push({child: collapse(x, y+1), action: 'down'})
  end
  if is_ok(x+1, y, grid, units)
    steps.push({child: collapse(x+1, y), action: 'right'})
  end
  if is_ok(x-1, y, grid, units)
    steps.push({child: collapse(x-1, y), action: 'left'})
  end
  if is_ok(x, y-1, grid, units)
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
  gamedata = tick(gamedata)
  display(gamedata)
  gamedata = tick(gamedata)
  display(gamedata)
  gamedata = tick(gamedata)
  display(gamedata)
  gamedata = tick(gamedata)
  display(gamedata)
  gamedata = tick(gamedata)
  display(gamedata)
end

begin_tests = Time.now
tests()
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

["input_tiny1.txt"].each do |x|
  puts "Part 1, target: #{x}"
  part1(x)
end
["input_small.txt"].each do |x|
  puts "Part 1, target: #{x}"
  part1(x)
end
