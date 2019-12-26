# Day 25: Cryostasis

## Approach and Reflections

This year ended with a text adventure game that runs on our intcode VMs! To
finish the game, you must collect the right set of items and pass through the
security checkpoint. It was fun, creative, and a great way to end the event.

To solve the game on the night of, I hooked up some basic I/O to my intcode VM
and played the game manually. I went back and later added an autosolver, which
uses DFS with save states to build a graph of the game map while noting the
location of all items. It then uses `networkx` to navigate throughout the
maze, picking up all items. (Why `networkx`? The basic info collected during
the initial DFS is only sufficient to plan paths starting from the root node.)

With all items, it heads to the security checkpoint and brute forces all
combinations of items to see which are allowed to pass.

Potential room for improvement: Some items should not be picked up and make
the game crash in creative ways. The VM could be programmed to save state and
try picking up an item, then restore and blacklist the item if it didn't
work. Instead, it uses a manually coded blacklist I created while playing the
game manually.

Another point of improvement would be to make the brute force item search at
the end a bit smarter. The game tells you if you're too heavy or too light,
so any combinations of items that contain subsets of items that are too heavy
on their own don't need to be tried.

## Solutions

- [Python](./python_day25/day25.py)

## Problem Description

[2019 Day 25 on AdventOfCode.com](https://adventofcode.com/2019/day/25)

### Part One

As you approach Santa's ship, your sensors report two important details:

First, that you might be too late: the internal temperature is -40 degrees.

Second, that one faint life signature is somewhere on the ship.

The airlock door is locked with a code; your best option is to send in a small
droid to investigate the situation. You attach your ship to Santa's, break
a small hole in the hull, and let the droid run in before you seal it up
again. Before your ship starts freezing, you detach your ship and set it to
automatically stay within range of Santa's ship.

This droid can follow basic instructions and report on its surroundings; you
can communicate with it through an Intcode program (your puzzle input) running
on an ASCII-capable computer.

As the droid moves through its environment, it will describe what it
encounters. When it says Command?, you can give it a single instruction
terminated with a newline (ASCII code 10). Possible instructions are:

- Movement via `north`, `south`, `east`, or `west`.
- To take an item the droid sees in the environment, use the command `take <name of item>`. For example, if the droid reports seeing a `red ball`, you
  can pick it up with take `red ball`.
- To drop an item the droid is carrying, use the command `drop <name of item>`. For example, if the droid is carrying a `green ball`, you can drop
  it with `drop green ball`.
- To get a list of all of the items the droid is currently carrying, use the
  command `inv` (for "inventory").

Extra spaces or other characters aren't allowed - instructions must be
provided precisely.

Santa's ship is a Reindeer-class starship; these ships use pressure-sensitive
floors to determine the identity of droids and crew members. The standard
configuration for these starships is for all droids to weigh exactly the same
amount to make them easier to detect. If you need to get past such a sensor,
you might be able to reach the correct weight by carrying items from the
environment.

Look around the ship and see if you can find the password for the main
airlock.

### Part Two

As you move through the main airlock, the air inside the ship is already
heating up to reasonable levels. Santa explains that he didn't notice you
coming because he was just taking a quick nap. The ship wasn't frozen; he just
had the thermostat set to "North Pole".

You make your way over to the navigation console. It beeps. "Status: Stranded.
Please supply measurements from 49 stars to recalibrate."

"49 stars? But the Elves told me you needed fifty--"

Santa just smiles and nods his head toward the window. There, in the distance,
you can see the center of the Solar System: the Sun!

The navigation console beeps again.
