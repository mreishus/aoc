# Advent Of Code 2018, Day 6

https://adventofcode.com/2018/day/6

Another grid problem.  I didn't have much trouble with this as I was already familiar with the Manhattan distance or L1 norm.

**Languages Solved In:** Ruby, Elixir

## Part 1

**Problem:** We have a 2d grid with some points.  Essentially, we want to find the point that would have the largest area in a Voronoi diagram computed with Manhattan distances, given that the area "isn't infinite" (doesn't touch the outside of the grid).

**Approach, Ruby+Elixir:**  Make a 2d array representing the grid.  Load the points into an array.  Loop over the entire grid, computing the Manhattan distance to each point, and store which coordinate is the closest in each point of the grid.  Also, if we're on the edge of the grid, set an "Is Infinite" flag.

Now, for each point, loop through the grid, looking for points that match, and add that to my area score.  Also, note if at least one point has the "is infinite flag".  We'll add the "area score" and "is infinite" columns to our list of points.

Now, pick the point that has the largest area score without an infinite flag.

## Part 2

**Problem:** There is a "safe area" where given a point on the grid, the sum of all Manhattan distances to all defined points is less than 10,000.  What is its area?

**Approaches:** Now, loop through the grid and compute the Manhattan distances to each point.  Sum them; if it's less than the 10,000 threshold add 1 to our "Safe Squares" count.

