#!/usr/bin/env ruby

require 'pp'
puts 'hi'

FILENAME = 'input.txt'
#FILENAME = 'input_small.txt'
GRID_SIZE = 250

def make_grid()
  grid = Array.new(GRID_SIZE) { Array.new(GRID_SIZE) }
  ## Build init grid
  x = 1
  y = 1
  File.readlines(FILENAME).each do |line|
    x = 1
    line.chars.each do |char|
      grid[y][x] = char
      x += 1
    end
    y += 1
  end
  grid
end

def find_carts(grid)
  carts = []
  0.upto(GRID_SIZE-1) do |y|
    0.upto(GRID_SIZE-1) do |x|
      cart = nil
      if grid[y][x] == 'v'
        grid[y][x] = "|"
        cart = {x: x, y: y, dir: 'v', turn_num: 0}
      elsif grid[y][x] == '^'
        grid[y][x] = "|"
        cart = {x: x, y: y, dir: '^', turn_num: 0}
      elsif grid[y][x] == '>'
        grid[y][x] = "-"
        cart = {x: x, y: y, dir: '>', turn_num: 0}
      elsif grid[y][x] == '<'
        grid[y][x] = "-"
        cart = {x: x, y: y, dir: '<', turn_num: 0}
      end

      if cart != nil
        carts.push cart
      end
    end
  end

  [grid, carts]
end

def scan_for_crashes(carts)
  z = carts.map{ |c| c[:x].to_s + "," + c[:y].to_s }
  if z.uniq.length != z.length
    qwer = z.group_by{ |e| e }.select { |k, v| v.size > 1 }.map(&:first)
    puts "Crash happened: "
    pp qwer
    puts "Make sure to subtract 1 for answer"
    raise 'crash!!'
  end
end

def tick(grid, carts)
  carts = carts.sort_by{|x| x[:y]}
  carts.each_with_index do |cart|
    if cart[:dir] == 'v'
      cart[:y] += 1
    elsif cart[:dir] == '^'
      cart[:y] -= 1
    elsif cart[:dir] == '<'
      cart[:x] -= 1
    elsif cart[:dir] == '>'
      cart[:x] += 1
    end

    scan_for_crashes(carts)

    this_square = grid[ cart[:y] ][ cart[:x] ]
    if this_square == "+"

      if cart[:turn_num] == 0
        turn = 'left'
      elsif cart[:turn_num] == 1
        turn = 'straight'
      elsif cart[:turn_num] == 2
        turn = 'right'
      end

      cart[:dir] = do_turn(turn, cart[:dir])

      cart[:turn_num] += 1
      if cart[:turn_num] == 3
        cart[:turn_num] = 0
      end

    elsif this_square == '/'

      if cart[:dir] == '>'
        cart[:dir] = '^'
      elsif cart[:dir] == 'v'
        cart[:dir] = '<'
      elsif cart[:dir] == '^'
        cart[:dir] = '>'
      elsif cart[:dir] == '<'
        cart[:dir] = 'v'
      end
    elsif this_square == '\\'

      if cart[:dir] == '>'
        cart[:dir] = 'v'
      elsif cart[:dir] == 'v'
        cart[:dir] = '>'
      elsif cart[:dir] == '^'
        cart[:dir] = '<'
      elsif cart[:dir] == '<'
        cart[:dir] = '^'
      end
    end
  end
  carts
end

def do_turn(turn, direction) 
  if turn == 'straight'
    return direction
  elsif turn == 'left'
    map = {
      "^" => "<",
      "<" => "v",
      "v" => ">",
      ">" => "^",
    };
    return map[direction];
  elsif turn == 'right'
    map = {
      "^" => ">",
      "<" => "^",
      "v" => "<",
      ">" => "v",
    };
    return map[direction];
  end
  direction
end

def print_map(grid, carts)
  0.upto(8) do |y|
    0.upto(GRID_SIZE-1) do |x|
      candidates = carts.select{ |c| c[:x] == x && c[:y] == y }
      if candidates.any?
        print candidates.first[:dir]
      else
        print grid[y][x]
      end
    end
    print "\n"
  end
  ''
end

def minus_one(carts)
  carts.map{ |c| (c[:x]-1).to_s + "," + (c[:y]-1).to_s }
end


def main
  grid = make_grid
  grid, carts = find_carts(grid)

  0.upto(1015) do |i|
    carts = tick(grid, carts)
    #pp '---'
    #pp minus_one(carts)
    #print_map(grid, carts)
  end
end

# Guesses: (You guessed 57,47.)

main
