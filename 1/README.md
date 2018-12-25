# Advent Of Code 2018, Day 1

Day 1 was relatively straightforward.   I have never programmed with Elixir before, and I had been interested in the language after watching its mini-documentary on youtube ( https://www.youtube.com/watch?v=lxYFOM3UJzo ), so I gave it a shot and wrote my first elixir programs ever.

## Part 1

**Problem:** Sum all numbers in a file.

**Approach:** Solved easily by reading in the file and piping to `Enum.sum`.

## Part 2

**Problem:** Keep a running sum of all numbers in a file, until a sum is repeated - that's the answer.  If no answer is found after summing all the numbers, read the file repeatedly until an answer is found.

**Approach:** I used `Enum.reduce` to build my own summing function.  But my accumulator did not only hold the sum;  it also contained a `seen_map`, where I track every sum that's been seen.   

As duplicates are found, I push them onto the `seen_multiple` array.  After each scan of the file, I check `seen_multiple` to see if we've found an answer and either return it or start another scan.  Because it's an array, I know which answer was found first.

**Downsides**:  Answer checks are only done after each file is scanned completely, so the program might do extraneous work, especially with large files. At the time, I didn't know how to make the `Enum.reduce` stop calculating early.  However, if I were to rewrite this, I might use pattern matching to make the accumulator contain a signal that it's done and to stop computing.

