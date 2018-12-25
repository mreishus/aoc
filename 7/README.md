# Advent Of Code 2018, Day 7

https://adventofcode.com/2018/day/7

Challenging, interesting problem.  The first "step up" in difficulty of this year's Advent of Code. 

**Languages Solved In:** Ruby, Elixir

## Part 1

**Problem:** We're given a list of task dependencies, like:

```
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
```

And must determine which order the tasks are completed in.

**Approach, Ruby+Elixir:**

Here, I stored the dependencies in a map likes so:
```
{
  "A" => ["C"],
  "E" => ["B", "D", "F"],
 ...
}
```
Meaning that E requires B D and F to be finished before running.  Then, I scanned the array looking for keys with value.length = 0, applying the tiebreaker if needed to find the next step.  After removing the next step from all hash values, we're ready to repeat the algorithm.

If run time was a problem, I could use a priority queue instead of a hash - but it wasn't a big deal here.

## Part 2

**Problem:**  Each of the tasks is assigned a run time according to its position in the alphabet. There are 5 workers available to work on tasks, so tasks may be done in parallel, but the dependency system mentioned earlier must still be satisfied. How long will it take to complete all the steps?

**Approaches:** I would call this the first "difficult" problem.  I created a simulation that started with time=0 and ticked through each second.  Each step, it would:

- Check to see if any tasks were finished and clear out those workers
- Delete finished tasks from the dependency hash
- Find out if any tasks were available to be started
- Loop through all idle workers and assign those tasks

I was beginning to feel like my Elixir program was a bit too hard to understand and perhaps not organized properly.  I wished for a type system to make it a bit more clear, or for more knowledge of Elixir to help better structure my programs.  From here on out, I would stop using Elixir and focus on a language that I already know well, Ruby, to develop solutions.

It took some effort, but it was fun to get working and to see it all come together.  

