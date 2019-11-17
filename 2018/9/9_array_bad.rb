#!/usr/bin/env ruby

require 'pp'

FILENAME = 'input.txt'
#FILENAME = 'input_small.txt'

#File.readlines(FILENAME).each do |line|
#end

max_players = 411
STOP_PLAYING_MARBLE = 72_059 * 100

players = []
player_score = {}
1.upto(max_players) do |i|
  players.push i
  player_score[i] = 0
end
pp players
pp player_score

marbles = [0]
selected_marble_index = 0
marble_to_insert = 1
current_player = 1
i = 1
while 1
  if marble_to_insert % 23 == 0
    #puts "Player notices the selected marble index is #{selected_marble_index} which is marble #{marbles[selected_marble_index]}"
    player_score[current_player] += marble_to_insert
    index_to_delete =
      (selected_marble_index - 7 + marbles.length) % marbles.length
    #puts "Player #{current_player} deletes marble #{marbles[index_to_delete]}"
    player_score[current_player] += marbles[index_to_delete]
    marbles.slice!(index_to_delete)
    selected_marble_index = index_to_delete
  else
    if marbles.length == 1 || marbles.length == 2
      selected_marble_index = 1
    elsif marbles.length == 3
      selected_marble_index = 3
    else
      selected_marble_index =
        (selected_marble_index + 2 + marbles.length) % marbles.length
      selected_marble_index = marbles.length if selected_marble_index == 0
    end

    ## Most of the time, insert
    marbles.insert(selected_marble_index, marble_to_insert)
    #puts "Player #{current_player} inserts marble #{marble_to_insert}"
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

  i += 1
  if (i > STOP_PLAYING_MARBLE)
    pp '--'
    pp player_score
    pp 'Max:'
    pp player_score.values.max
    exit
  end
end

a = %w[a b c d]
a.insert(2, 99) #=> ["a", "b", 99, "c", "d"]
a.insert(-20, 1, 2, 3) #=> ["a", "b", 99, "c", 1, 2, 3, "d"]
pp a
