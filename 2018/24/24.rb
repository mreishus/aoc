#!/usr/bin/env ruby

require 'pp'
require 'duplicate'

class Fighter
  attr_accessor :id, :num, :hp, :atk_p, :atk_t, :init, :army, :immunes, :weaks, :target
  def initialize(id, num, hp, atk_p, atk_t, init, army)
    @id = id
    @num = num
    @hp = hp
    @atk_p = atk_p
    @atk_t = atk_t
    @init = init
    @army = army
    @target = nil
  end

  def effective_power
    @num * @atk_p
  end
end

def parse_file(filename)
  fighters = []
  army = nil
  id = 0
  File.readlines(filename).each do |line|
    if line =~ /^Immune System/
      army = 0
      next
    end
    if line =~ /^Infection/
      army = 1
      next
    end

    main_re = /(\d+) units each with (\d+) hit points.*with an attack that does (\d+) (\w+) damage at initiative (\d+)/
    next unless line =~ main_re
    num, hp, atk_p, atk_t, init = line.strip.match(main_re).captures

    immunes = []
    weaks = []
    immune_re = /immune to (.*?)[;\)]/
    weak_re = /weak to (.*?)[;\)]/
    if line =~ immune_re
      immune_str, = line.match(immune_re).captures
      immunes = immune_str.split(", ")
      #puts "Immunes: #{immunes}"
    end
    if line =~ weak_re
      weak_str, = line.match(weak_re).captures
      weaks = weak_str.split(", ")
      #puts "Weaks: #{weaks}"
    end

    f = Fighter.new(id, num.to_i, hp.to_i, atk_p.to_i, atk_t, init.to_i, army)
    id += 1
    f.immunes = immunes
    f.weaks = weaks

    #puts line
    #pp f

    fighters.push f
  end
  fighters
end

def tick(fighters_in)
  tick_attack(tick_target_selection(fighters_in))
end

def tick_target_selection(fighters_in)
  fighters_out = Duplicate.duplicate(fighters_in)

  # Clear all targets
  fighters_out.each do |f|
    f.target = nil
  end

  # Armys take turn selecting targets - Dont think it works this way
  #[0, 1].each do |army|
  #  troops = fighters_out.select{ |x| x.army == army}.sort_by { |x| [x.effective_power, x.init] }.reverse
  #  troops.each do |t|
  #    t.target = select_target(t, fighters_out)
  #  end
  #end

  troops = fighters_out.sort_by { |x| [x.effective_power, x.init] }.reverse
  troops.each do |t|
    #puts "-----------Selecting target #{t.effective_power} #{t.init}"
    t.target = select_target(t, fighters_out)
  end

  fighters_out
end

def select_target(attacking, fighters)
  units_being_targeted = fighters.map{ |x| x.target }
  enemies = fighters.select { |x| x.army != attacking.army && !units_being_targeted.include?(x.id) }
  target = enemies.max_by { |e| [damage_done(attacking, e), e.effective_power, e.init] }
  return nil if damage_done(attacking, target).zero?

  target.id
end

def damage_done(attacking, target)
  # If attacking has 0 or negative units, then 0 dmg
  # If defender Immune, then 0
  #return 0 if attacking.num <= 0
  return 0 if target.nil?
  return 0 if target.immunes.include?(attacking.atk_t)

  #print "Calculating damage .. Num[#{attacking.num}] AP[#{attacking.atk_p}] EP[#{attacking.effective_power}] "
  dmg = attacking.effective_power

  if target.weaks.include?(attacking.atk_t)
    #print " Weaks: #{target.weaks}"
    #print " Attack: #{attacking.atk_t} "
    #puts " WEAK 2x[#{dmg*2}]"
  else
    #puts " 1x[#{dmg}]"
  end
  return dmg*2 if target.weaks.include?(attacking.atk_t)

  dmg
end

def tick_attack(fighters_in)
  fighters_out = Duplicate.duplicate(fighters_in)

  troop_ids = fighters_out.sort_by { |x| x.init }.reverse.map { |x| x.id }
  troop_ids.each do |attacking_id|
    attacking = fighters_out.find { |e| e.id == attacking_id }
    next if attacking.num <= 0 || attacking.target.nil? # dead
    target = fighters_out.find { |e| e.id == attacking.target }
    raise 'Invalid target' if target.nil?

    damage = damage_done(attacking, target)
    units_killed = damage / target.hp

    #puts "Id #{attacking.id} Attacks #{target.id}, damage[#{damage}] Kills[#{units_killed}]"
    #puts "     Victim num before: #{target.num}"
    target.num -= units_killed
    #puts "     Victim num after: #{target.num}"
  end

  fighters_out.reject! { |y| y.num <= 0 } # Remove Dead

  fighters_out
end

def display(fighters)
  #puts 'Immune System:'
  troops = fighters.select { |x| x.army == 0 }.sort_by { |x| x.id }
  troops.each do |t|
    #puts "Group #{t.id} Contains #{t.num} Units"
  end
  #puts 'Infection:'
  troops = fighters.select { |x| x.army == 1 }.sort_by { |x| x.id }
  troops.each do |t|
    #puts "Group #{t.id} Contains #{t.num} Units"
  end
  #puts
end

def one_side_dead(fighters)
  return true if fighters.select { |x| x.army == 0 } .count == 0
  return true if fighters.select { |x| x.army == 1 } .count == 0
  false
end

def part1
  fighters = parse_file('input.txt')
  #fighters = parse_file('input_small.txt')
  display(fighters)
  #pp fighters
  #raise 'test'
  loop do
    fighters = tick(fighters)
    display(fighters)
    break if one_side_dead(fighters)
  end
  puts "Over.."
  puts fighters.select{ |x| x.num > 0}.map{ |x| x.num }.sum
end

def apply_boost(fighters, boost)
  fighters.select { |x| x.army == 0 }.each do |f|
    f.atk_p += boost
  end
  fighters
end

def simulate_fight(filename, boost)
  fighters = parse_file(filename)
  fighters = apply_boost(fighters, boost)

  last_sums = [1, 2, 3, 4, 5, 6, 7, 8]
  loop do
    fighters = tick(fighters)
    display(fighters)
    break if one_side_dead(fighters)

    sum = fighters.map{ |x| x.num }.sum
    last_sums.shift
    last_sums.push sum
    break if last_sums[last_sums.length - 1] == last_sums[last_sums.length - 2] && last_sums[last_sums.length - 1] == last_sums[last_sums.length - 3] && last_sums[last_sums.length - 1] == last_sums[last_sums.length - 4]
  end

  fighters_left = fighters.select{ |x| x.num > 0}.map{ |x| x.num }.sum

  return ["infection", fighters_left] if fighters.select { |x| x.army == 0 } .count == 0
  return ["immune", fighters_left] if fighters.select { |x| x.army == 1 } .count == 0
  ["stalemate", fighters_left]
end

raise 'f1' unless simulate_fight('input_small.txt', 0) == ['infection', 5216]
raise 'f2' unless simulate_fight('input_small.txt', 1570) == ['immune', 51]

1.upto(10000) do |b|
  puts b
  winner, sum = simulate_fight('input.txt', b)
  if winner == 'immune'
    puts "Immune wins!  Sum is #{sum} Boost is #{b}"
    break
  end
end
