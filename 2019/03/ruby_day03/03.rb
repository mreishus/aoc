#!/usr/bin/env ruby
$DIRECTIONS = {
  'R' => Complex(1, 0),
  'L' => Complex(-1, 0),
  'U' => Complex(0, 1),
  'D' => Complex(0, -1)
}

# Input (String): "L1003,U125,L229,U421"
# Output (Wire): [["L", 1003], ["U", 125], ["L", 229], ["U", 421]]
def parse_wire(line)
  line.split(',').map do |pair|
    compass, l = pair.match(/^(\w)(\d+)$/).captures
    [compass, l.to_i]
  end
end

# Input (filename: String) -> Output (List of Wires)
def parse(filename)
  File.readlines(filename).map { |line| parse_wire(line) }
end

def manhattan(coord)
  coord.real.abs + coord.imaginary.abs
end

def total_steps(grid_value)
  grid_value.map { |info| info[:total_steps] }.sum
end

def part12(data)
  grid = Hash.new(nil)
  data.each_with_index do |wire, wire_index|
    location = Complex(0, 0)
    total_steps = 0
    wire.each do |step|
      delta = $DIRECTIONS[step[0]]
      1.upto(step[1]) do |i|
        location += delta
        total_steps += 1
        info = { wire_index: wire_index, total_steps: total_steps }
        # puts "i #{i} location #{location} wire #{wire_index}"

        if grid[location] == nil
          grid[location] = [info]
        elsif !grid[location].any? { |thing| thing[:wire_index] == wire_index }
          grid[location].push(info)
        end
      end
    end
  end

  intersections = grid.keys.filter { |k| grid[k].length >= 2 }
  answer1 = intersections.map { |k| manhattan(k) }.min
  answer2 = intersections.map { |k| total_steps(grid[k]) }.min

  [answer1, answer2]
end

data = parse('../input.txt')
answers = part12(data)
puts 'Part 1:'
puts answers[0]
puts 'Part 2:'
puts answers[1]
