# Day 23: Coprocessor Conflagration

## Approach and Reflections

We're asked to implement a simple VM; then we're given a program that will run
forever and asked to find what its final output would be if it ever finished
running.

OK, the disassembly problem! I'd done one previously in the 2018 event, so
I knew a little bit of what to expect. First, I changed the VM to print what
instruction it's working on, then I let it run for a while and captured the
output to see what loop it's stuck on.

I optimized that inner loop, first by causing all of its expressions to happen
in one step, then later by executing the loop itself in elixir, not the VM.
This made it faster, but it still wasn't fast enough: A second, outer loop was
taking up most of the time.

The two loops run and set a certain variable (`f`) if a condition met, so
I changed both loops to exit early if they set the variable. This sped up
most cases, but there were a few cases where the variables were not being set,
and the loops would run for too long. I changed both loops to run in elixir,
but it was still too slow.

By the time I implemented both loops in elixir, I realized what the VM was
doing, so I was able to implement it directly in my code with a more efficient
algorithm. (I'm being deliberately obtuse as to not spoil the entire problem.)

## Solutions

- [Elixir](./elixir_day23/lib/vm.ex)

## Problem Description

[2017 Day 23 on AdventOfCode.com](https://adventofcode.com/2017/day/23)

### Part 1

You decide to head directly to the CPU and fix the printer from there. As you
get close, you find an experimental coprocessor doing so much work that the
local programs are afraid it will halt and catch fire. This would cause
serious issues for the rest of the computer, so you head in and see what you
can do.

The code it's running seems to be a variant of the kind you saw recently on
that tablet. The general functionality seems very similar, but some of the
instructions are different:

- set X Y sets register X to the value of Y.
- sub X Y decreases register X by the value of Y.
- mul X Y sets register X to the result of multiplying the value contained in
  register X by the value of Y.
- jnz X Y jumps with an offset of the value of Y, but only if the value of
  X is not zero. (An offset of 2 skips the next instruction, an offset of -1
  jumps to the previous instruction, and so on.)

  Only the instructions listed above are used. The eight registers here,
  named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for
testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul
instruction invoked?

### Part 2

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch,
which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program
obviously didn't choose a very efficient implementation. You'll need to
optimize the program if it has any hope of completing before Santa needs that
printer working.

The coprocessor's ultimate goal is to determine the final value left in
register h once the program completes. Technically, if it had that... it
wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what
value would be left in register h?
