#!/usr/bin/env ruby

require 'pp'

#FILENAME = 'input.txt'
FILENAME = 'input_small.txt'

def is_star(stars, x, y)
  stars.select{ |s| s[:posx] == x && s[:posy] == y }.count > 0
end

def advance_stars(stars)
  stars.each do |s|
    s[:posx] += s[:velx]
    s[:posy] += s[:vely]
  end
  stars
end

stars = []
File.readlines(FILENAME).each do |line|
  posx, posy, velx, vely = line
    .match(/position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>/i)
    .captures.map{ |x| x.to_i }
  star = {posx: posx, posy: posy, velx: velx, vely: vely}
  stars.push(star)
end

pp stars.select{ |s| s[:posy] == 0 }

1.upto(100000) do |time|
  x_center = stars.map{ |s| s[:posx] }.sum.fdiv(stars.size)
  y_center = stars.map{ |s| s[:posy] }.sum.fdiv(stars.size)

  x_var = (stars.map{ |s| (s[:posx] - x_center) ** 2 }.sum) / stars.count
  y_var = (stars.map{ |s| (s[:posy] - y_center) ** 2 }.sum) / stars.count

  #show = (x_var + y_var) < 700
  show = (x_var + y_var) < 50

  if (show)
    puts "time #{time} center (#{x_center}, #{y_center}) var (#{x_var}, #{y_var})" if show

    x_show_min = (x_center - 40).round
    x_show_max = (x_center + 40).round
    y_show_min = (y_center - 20).round
    y_show_max = (y_center + 20).round

    y_show_min.upto(y_show_max) do |y|
      x_show_min.upto(x_show_max) do |x|
        if (is_star(stars, x, y))
          print '#'
        else
          print '.'
        end
      end
      print "\n"
    end
  end
  print "\n" if show
  print time.to_s + "\n" if show
  stars = advance_stars(stars)
  if (time % 1000 == 0)
    #pp stars
  end
end


#pp stars
