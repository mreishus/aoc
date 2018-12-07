#!/usr/bin/env ruby
FILENAME = 'input.txt'
#FILENAME = 'input_small.txt'

def do_next(deps)
  cands = []
  deps.each do |key, val|
    if val.length == 0
      cands.push(key)
    end
  end
  cands.sort.first
  #pp '-----'
  #z = deps.sort_by {|key, value| value.length}
  ##zz = z.filter{|x| x[1].length == 0}
  #pp 'z:'
  #pp z
  #pp '-----'
  #deps.sort_by {|key, value| value.length}.first.first
end

require 'pp'
deps = {}
File.readlines(FILENAME).each do |line|
  fir, nex = line.match(/Step (\w+) must be finished before step (\w+) can begin./i).captures

  if !deps.has_key?(fir)
    deps[fir] = []
  end
  if !deps.has_key?(nex)
    deps[nex] = []
  end

  deps[nex].push(fir)
end

order = []
pp deps
pp deps.keys.length
while deps.keys.length > 0 do
  next_step = do_next(deps)
  order.push(next_step)

	deps.each do |key, val|
    deps[key] = val.reject{|x| x == next_step}
	end


  deps.delete(next_step)
end

pp order
puts order.join

#a = deps.sort_by {|key, value| value.length}.first.first
#pp deps
#pp a
