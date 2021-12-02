#!/usr/bin/env perl
use 5.010;
while (<>) {
    /forward (\d+)/ and $x += $1, $y2 += ($aim * $1);
    /down (\d+)/    and $y += $1, $aim += $1;
    /up (\d+)/      and $y -= $1, $aim -= $1;
}
say $x * $y;
say $x * $y2;
