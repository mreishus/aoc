# Day 20: Firewall Rules

## Approach and Reflections

We're given a list of number ranges, then asked to find the first number not
in any range, then the amount of numbers not in any range.

The Naive algorithm would loop over all numbers, then loop over all ranges for
each number, checking for at least one match. I knew that would be way too
slow, so I avoided it.

Instead, I sorted the number ranges by ascending lowest number, then looped
over the list of ranges once, keeping a "high watermark" of the highest high
range number I've seen so far, and comparing it to the next low range number
I see, looking for gaps.

## Solutions

- [Elixir](../elixir2016/lib/day20.ex)

## Problem Description

[2016 Day 20 on AdventOfCode.com](https://adventofcode.com/2016/day/20)

### Part 1

You'd like to set up a small hidden computer here so you can use it to get back
into the network later. However, the corporate firewall only allows
communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems
to be messy and poorly maintained, and it's not clear which IPs are allowed.
Also, rather than being written in dot-decimal notation, they are written as
plain 32-bit integers, which can have any value from 0 through 4294967295,
inclusive.

For example, suppose only the values 0 through 9 were valid, and that you
retrieved the following blacklist:

```
5-8
0-2
4-7
```

The blacklist specifies ranges of IPs (inclusive of both the start and end
value) that are not allowed. Then, the only IPs that this firewall allows are 3
and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle
input), what is the lowest-valued IP that is not blocked?

### Part 2

How many IPs are allowed by the blacklist?
