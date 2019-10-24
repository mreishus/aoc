#!/usr/bin/env ruby

require 'pp'

class Node
  attr_accessor :value
  attr_accessor :prev
  attr_accessor :next
end

#FILENAME = 'input.txt'
#FILENAME = 'input_small.txt'

#File.readlines(FILENAME).each do |line|
#end

max_players = 411
STOP_PLAYING_MARBLE = 72059 * 100
#STOP_PLAYING_MARBLE = 11

players = []
player_score = {}
1.upto(max_players) do |i|
  players.push i
  player_score[i] = 0
end
pp players
pp player_score

#marbles = [0]
#selected_marble_index = 0

marble_0 = Node.new
marble_0.value = 0

marble_1 = Node.new
marble_1.value = 1

marble_2 = Node.new
marble_2.value = 2

marble_0.next = marble_1
marble_1.next = marble_2
marble_2.next = marble_0

marble_0.prev = marble_2
marble_1.prev = marble_0
marble_2.prev = marble_1

selected_marble = marble_2

marble_to_insert = 3
current_player = 3
i = 3
while 1

  if marble_to_insert % 23 == 0
    #puts "Player notices the selected marble index is #{selected_marble_index} which is marble #{marbles[selected_marble_index]}"
    player_score[current_player] += marble_to_insert

    seven_minus = selected_marble.prev.prev.prev.prev.prev.prev.prev
    six_minus = seven_minus.next
    eight_minus = seven_minus.prev


    #puts "Player #{current_player} deletes marble #{marbles[index_to_delete]}"
    player_score[current_player] += seven_minus.value
    eight_minus.next = six_minus
    six_minus.prev = eight_minus

    selected_marble = six_minus

    #index_to_delete = selected_marble_index - 7
    #marbles.slice!(index_to_delete)
    #selected_marble_index = index_to_delete
  else

    new_marb = Node.new
    new_marb.value = marble_to_insert

    one_plus = selected_marble.next
    two_plus = selected_marble.next.next

    one_plus.next = new_marb
    two_plus.prev = new_marb
    new_marb.prev = one_plus
    new_marb.next = two_plus

    selected_marble = new_marb

  end

  #pp '--'
  #pp current_player
  #pp marbles
  #pp "selected: #{marbles[selected_marble_index]}"


  ## End of loop, increment and set up for next loop

  # This looks dumb but it works
  current_player = (current_player % (max_players)) + 1 

  #
  marble_to_insert += 1

  if (i % 10000 == 0)
    puts "Mrable #{i} #{i.to_f / STOP_PLAYING_MARBLE}"
  end

  i += 1
  if (i > STOP_PLAYING_MARBLE)
    pp '--'
    pp player_score
    pp "Max:"
    pp player_score.values.max
    exit
  end
end

