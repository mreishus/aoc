# Advent Of Code 2018, Day 3

https://adventofcode.com/2018/day/3

The first of many grid-based problems in this year's Advent of code.  Here, my lack of experience with Elixir was beginning to show:  I reached for Ruby first, then Elixir.

**Languages Solved In:** Ruby, Elixir

## Part 1

**Problem:** Given a list of claims (square patches) on a grid, how many squares are overlapped by two or more patches?

**Approach, Ruby:** Build a 2d array representing the grid.  Each square of the grid is another array representing the claims covering that square.  

Loop over the claims, marking them in the grid.  Then loop over every coordinate of the grid, checking to see which have more than 1 claim.

**Approach, Elixir:** I didn't know how to apply claims to the grid in a functional style at first.  I eventually went with nested `Enum.reduce`s wrapping calls to `Map.get_and_update`, which allowed me to traverse the grid and update it square by square while respecting immutability.

## Part 2

**Problem:** There is only one claim that doesn't overlap.  What is its ID?

**Approach, Ruby:** After building up the grid, I created a `non_overlapping_ids` array which had all arrays.  Then I scanned over every coordinate of the board, looking for squares with overlapping claims.  When found, I removed all of those claims from the `non_overlapping_ids` array.  After the scan completed, it had the answer.

**Approach, Elixir**:  Same approach as Ruby, but in a functional style.  I once again used nested `Enum.reduce`, but this time my accumulator was a list of non overlapping claims.

