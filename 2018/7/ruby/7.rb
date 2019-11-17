#!/usr/bin/env ruby
FILENAME = 'input.txt'
EXTRA_TIME = 60
#FILENAME = 'input_small.txt'
#EXTRA_TIME = 0

def do_next(deps)
  cands = []
  deps.each { |key, val| cands.push(key) if val.length == 0 }
  ##pp cands
  cands.sort
  #pp '-----'
  #z = deps.sort_by {|key, value| value.length}
  ##zz = z.filter{|x| x[1].length == 0}
  #pp 'z:'
  #pp z
  #pp '-----'
  #deps.sort_by {|key, value| value.length}.first.first
end

def time_to_do(letter)
  letter.ord - 64 + EXTRA_TIME
end

require 'pp'
deps = {}
File.readlines(FILENAME).each do |line|
  fir, nex =
    line.match(/Step (\w+) must be finished before step (\w+) can begin./i)
      .captures

  deps[fir] = [] if !deps.has_key?(fir)
  deps[nex] = [] if !deps.has_key?(nex)

  deps[nex].push(fir)
end

# Init Workers
workers = []
1.upto(5) do
  worker = { working_on: nil, done_on_second: nil }
  workers.push(worker)
end

order = []
pp deps
pp deps.keys.length

sec = 0
while deps.keys.length > 0
  puts "Second #{sec} started"
  ## Did anyone finish anything?
  what_was_finished = []

  ## Find out what was finished and clear out that worker
  workers.each_with_index do |x, i|
    if x[:done_on_second] == sec && x[:working_on] != nil
      puts "  -- Clearing out worker #{i}"
      what_was_finished.push(x[:working_on])
      order.push(x[:working_on])
      x[:working_on] = nil
      x[:done_on_second] = nil
    end
  end

  ## Delete stuff that was finished
  what_was_finished.each do |finished|
    puts "  -- Deleting #{finished}"
    deps.each { |key, val| deps[key] = val.reject { |x| x == finished } }
    deps.delete(finished)
  end

  ## What can be done next?
  next_steps = do_next(deps)
  ## What are people currently working on?
  working_on = workers.map { |x| x[:working_on] }

  ## If we're working on something remove it from next steps
  working_on.each { |x| next_steps.reject! { |y| y == x } }

  ## If next steps has something in it, assign it to the first available worker
  workers.each_with_index do |x, i|
    if x[:working_on] == nil && next_steps.length > 0
      x[:working_on] = next_steps.shift
      x[:done_on_second] = sec + time_to_do(x[:working_on])
      puts " +++ Assigning #{x[:working_on]} to worker #{
             i
           }, will be done on second #{x[:done_on_second]} "
    end
  end

  # Increment time
  sec += 1
end

#while deps.keys.length > 0 do
#  next_step = do_next(deps)
#  order.push(next_step)
#
#	deps.each do |key, val|
#    deps[key] = val.reject{|x| x == next_step}
#	end
#  deps.delete(next_step)
#
#
#end

puts 'Seconds:'
pp sec
#pp order
puts order.join

#a = deps.sort_by {|key, value| value.length}.first.first
#pp deps
#pp a

# Guessed 1235, didn't work -- It was 1234 LOL, off by one error
