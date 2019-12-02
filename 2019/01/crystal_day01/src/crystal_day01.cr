module CrystalDay01
  VERSION = "0.1.0"

  def self.parse_file(filename)
    File.read_lines(filename).map { |line| line.strip.to_i }
  end

  def self.fuel(num)
    (num // 3) - 2
  end

	def self.total_fuel(num)
		total_fuel = 0
		fuel = num
		loop do
			fuel = (fuel // 3) - 2
			break if fuel <= 0
			total_fuel += fuel
		end
		total_fuel
	end

  def self.part1(filename)
    parse_file(filename).map { |num| fuel(num) }.reduce { |num, acc| num + acc }
  end

	def self.part2(filename)
		parse_file(filename).map { |num| total_fuel(num) }.reduce { |num, acc| num + acc }
	end
end
