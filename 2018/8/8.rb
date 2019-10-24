#!/usr/bin/env ruby

require 'pp'

FILENAME = 'input.txt'
#FILENAME = 'input_small.txt'

nums = []
File.readlines(FILENAME).each do |line|
  nums = line.split(" ")
  nums = nums.map{ |x| x.to_i }
  break
end

def build_child(nums)
  node = {}

  num_children = nums.shift
  num_metadata = nums.shift
  node[:num_children] = num_children
  node[:num_metadata] = num_metadata
  children = []
  metadata = []

  1.upto(num_children) do |child_i|
    children.push( build_child( nums ) )
  end
  node[:children] = children

  1.upto(num_metadata) do |metadata_i|
    metadata.push( nums.shift )
  end
  node[:metadata] = metadata

  node
end

def add_all_metadata(tree)
  child_sum = tree[:children].map{ |x| add_all_metadata(x) }.sum
  tree[:metadata].sum + child_sum
end

def node_value(tree)
  #puts 'enter node value'
  #pp tree
  if (tree[:children].length == 0)
    #puts "return simple sum #{tree[:metadata].sum}"
    return tree[:metadata].sum
  end

  rv = 0

  tree[:metadata].each do |i|
    if tree[:children][i - 1] != nil
      rv += node_value(tree[:children][i - 1])
    end
  end

  #puts "return return value #{rv}"
  rv
end

tree = build_child(nums)
#pp tree
pp'--'
total = add_all_metadata(tree)
pp total
pp 'part2---'
pp node_value(tree)



