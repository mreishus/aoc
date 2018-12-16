#!/usr/bin/env ruby

class Time
  def to_ms
    (self.to_f * 1000.0).to_i
  end
end

require 'pp'

def tests
  raise 'fail' unless true == true
  test_input_tiny3
  test_input_tiny2
  test_input_small_move
  test_combat0
end

def test_combat0
  raise 'fail combat0' unless part1('input_combat0.txt') == 27730
  raise 'fail combat1' unless part1('input_combat1.txt') == 36334
  raise 'fail combat2' unless part1('input_combat2.txt') == 39514
  raise 'fail combat3' unless part1('input_combat3.txt') == 27755
  raise 'fail combat4' unless part1('input_combat4.txt') == 28944
  raise 'fail combat5' unless part1('input_combat5.txt') == 18740
end

def test_input_tiny2
  filename = "input_tiny2.txt"
  gamedata = readfile(filename)
  board_init = display_string(gamedata)

  gamedata = tick(gamedata)
  board_p1 = display_string(gamedata)

  p1_expect = %(
#######
#.EG..#
#.G.#.#
#...#G#
#######
)
  p1_expect[0] = ''
  raise 'fail 1 tiny2' unless p1_expect == board_p1
end

def test_input_tiny3
  filename = "input_tiny3.txt"
  gamedata = readfile(filename)
  board_init = display_string(gamedata)

  gamedata = tick(gamedata)
  board_p1 = display_string(gamedata)

  p1_expect = %(
#######
#..E..#
#...G.#
#.....#
#######
)
  p1_expect[0] = ''
  raise 'fail 1 tiny3' unless p1_expect == board_p1
end

def test_input_small_move
  filename = "input_small.txt"
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

  init_expect = %(
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
)
  p1_expect = %(
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########
)
  p2_expect = %(
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########
)
  p3_expect = %(
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########
)
  init_expect[0] = '' # remove extra newlines
  p1_expect[0] = ''
  p2_expect[0] = ''
  p3_expect[0] = ''
  p4_expect = p3_expect # No one can move
  raise 'fail 0 small' unless init_expect == board_init
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
  grid = Array.new(max_x + 1) { Array.new(max_y + 1) }
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
        unit = { x: x, y: y, type: 'gob', display: 'G', id: unit_id, hp: 200, atk: 3, alive: true }
        unit_id += 1
        units.push unit
      elsif c == 'E'
        grid[x][y] = '.'
        unit = { x: x, y: y, type: 'elf', display: 'E', id: unit_id, hp: 200, atk: 3, alive: true }
        unit_id += 1
        units.push unit
      elsif c == '.'
        grid[x][y] = '.'
      end
      x += 1
    end
    y += 1
  end
  { grid: grid, units: units, max_x: max_x, max_y: max_y, game_over: false }
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
  print display_string(gamedata)
end

# INPUT: gamedata
# OUTPUT: Prints board to string
def display_string(gamedata)
  grid, units, max_x, max_y = gamedata.values_at(:grid, :units, :max_x, :max_y)
  output = ''

  0.upto(max_y - 1) do |y|
    0.upto(max_x - 1) do |x|
      unit = units.find { |u| x.to_i == u[:x] && y.to_i == u[:y] }
      output += unit.nil? ? grid[x][y] : unit[:display]
    end
    output += "\n"
  end
  output
end

def tick(input_gamedata)
  gamedata = input_gamedata.dup
  units = gamedata[:units]
  turn_order = units.sort_by { |h| [h[:y].to_i, h[:x].to_i] }.map { |u| u[:id] }
  turn_order.each do |id|
    gamedata = tick_unit(gamedata, id)
    gamedata = remove_dead(gamedata)
    break if gamedata[:game_over]
  end
  gamedata
end

def remove_dead(input_gamedata)
  gamedata = input_gamedata.dup
  gamedata[:units] = gamedata[:units].select { |u| u[:alive] }
  gamedata
end

def collapse(x, y)
  x.to_s + '_' + y.to_s
end

def expand(xystring)
  xystring.split('_').map(&:to_i)
end

def tick_unit(input_gamedata, id)
  gamedata = tick_unit_move(input_gamedata, id)
  return gamedata if gamedata[:game_over]
  tick_unit_attack(gamedata, id)
end

def unit_exists(units, x, y)
  unit = units.find { |u| u[:x] == x && u[:y] == y }
  !unit.nil?
end

def tick_unit_move(input_gamedata, id)
  gamedata = input_gamedata.dup
  grid, units = gamedata.values_at(:grid, :units)
  unit = units.find { |u| u[:id] == id }
  return input_gamedata if unit.nil? || !unit[:alive]

  # how many enemies?
  enemies = units.reject { |u| u[:type] == unit[:type] }
  if enemies.count.zero?
    gamedata[:game_over] = true
    return gamedata
  end

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

  # Don't htink this helps?
  in_range = in_range.reject { |coord| unit_exists(units, coord[:x], coord[:y]) }

  problem = { grid: grid, units: units, unit: unit, targets: in_range }
  bfs(problem)

  ## Now we have to find the appropriate target
  move_to = problem[:targets]
    .reject { |t| t[:range].nil? }
    .sort_by { |t| t[:range] }

  return gamedata if move_to.empty? # Found no reachable targets

  tick_unit_move_doit(unit, move_to)
  gamedata
end

## Actually makes "unit" move according to "move_to"
## Side effect warning: Modifies Unit
def tick_unit_move_doit(unit, move_to)
  shortest_range = move_to.first[:range]
  move_to = move_to
            .select { |t| t[:range] == shortest_range } # Nearest only
            .min_by { |t| [t[:y], t[:x]] }              # First by reading order
  paths = move_to[:paths]

  if paths.select { |p| p.first == 'up'}.any?
    unit[:y] -= 1
  elsif paths.select { |p| p.first == 'left'}.any?
    unit[:x] -= 1
  elsif paths.select { |p| p.first == 'right'}.any?
    unit[:x] += 1
  elsif paths.select { |p| p.first == 'down'}.any?
    unit[:y] += 1
  end
end

def tick_unit_attack(input_gamedata, id)
  gamedata = input_gamedata.dup
  grid, units = gamedata.values_at(:grid, :units)
  unit = units.find { |u| u[:id] == id }
  return input_gamedata if unit.nil? || !unit[:alive]

  x = unit[:x]
  y = unit[:y]

  enemies = units.reject { |u| u[:type] == unit[:type] }
  adj_units = enemies.select do |u|
    (u[:x] == x + 1 && u[:y] == y) \
    || (u[:x] == x - 1 && u[:y] == y) \
    || (u[:x] == x && u[:y] == y + 1) \
    || (u[:x] == x && u[:y] == y - 1)
  end
  
  return gamedata if adj_units.empty?
  to_attack = adj_units.min_by { |t| [t[:hp], t[:y], t[:x]] }

  to_attack[:hp] -= unit[:atk]
  to_attack[:alive] = to_attack[:hp] > 0

  gamedata
end

# Breadth first search
# INPUT: problem wiht keys of :unit, :targets, :grid
# - We are looking to move unit towards one of the targets, constrained by grid
# OUTPUT:  modifies its arguments by putting information on problem[:targets]
# - Sets :range, :paths and :reachable on targets
def bfs(problem)
  unit, targets = problem.values_at(:unit, :targets)
  #pp unit
  #pp targets

  open_set = [collapse(unit[:x], unit[:y])]
  closed_set = []
  meta = {}
  min_range = nil
  steps_without_finding = 0

  while open_set.count > 0
    subtree_root = open_set.pop
    #puts "#{open_set.count} #{closed_set.count}"

    if goal?(problem, subtree_root)
      path = construct_path(subtree_root, meta)
      range = path.length
      node_x, node_y = expand(subtree_root)
      t = targets.find { |tg| tg[:x] == node_x && tg[:y] == node_y }
      t[:paths].push path unless t[:paths].include? path
      t[:range] = range if t[:range].nil? || t[:range] > range
      min_range = range if min_range.nil? || range < min_range
      t[:reachable] = true
      #puts "Writing range #{t[:range]}"
      steps_without_finding = 0
      #puts "--- early" if range > min_range # return early, we have already seen all the shortest paths..
      return if range > min_range # return early, we have already seen all the shortest paths..
    end

    steps_without_finding += 1

    get_possible_steps(problem, subtree_root).each do |step|
      child, action = step.values_at(:child, :action)
      next if closed_set.include? child

      meta[child] = [subtree_root, action]
      open_set.unshift(child)
    end

    #puts "no find: #{steps_without_finding}" if steps_without_finding % 500 == 0
    if false && steps_without_finding % 20000 == 0
      puts 'closed_set'
      pp closed_set
      puts 'open_set'
      pp open_set
    end
    closed_set.push(subtree_root) if !closed_set.include? subtree_root
  end
end

def construct_path(node, meta)
  actions = []

  until meta[node].nil?
    node, action = meta[node]
    actions.push(action)
  end
  actions.reverse
end

def goal?(problem, subtree_root)
  x, y = expand(subtree_root)
  targets = problem[:targets]
  targets.find { |t| t[:x] == x && t[:y] == y } != nil
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
  i = 0
  while true do
    gamedata = tick(gamedata)
    puts i
    display(gamedata)
    if gamedata[:game_over]
      break
    end
    i += 1
  end
  hp_sum = gamedata[:units].map{ |u| u[:hp] }.sum
  hp_sum * i
end

begin_tests = Time.now
tests
end_tests = Time.now
puts "All tests passed - #{end_tests.to_ms - begin_tests.to_ms}ms"

['input.txt'].each do |x|
  puts "Part 1, filename: #{x}"
  puts part1(x)
end
