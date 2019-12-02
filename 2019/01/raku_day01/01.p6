#!/usr/bin/env perl6

sub fuel($num --> Int) {
    return floor($num / 3) - 2;
}

sub total_fuel($weight --> Int) {
    my $total = 0;
    my $num = $weight;
    while (1) {
        $num = fuel($num);
        if ($num <= 0) {
            last;
        }
        $total += $num;
    }
    return $total;
}

sub part1(@data --> Int) {
    (@data.map: { fuel($_) }).sum;
}

sub part2(@data --> Int) {
    (@data.map: { total_fuel($_) }).sum;
}


my @data = map *.trim, "../input.txt".IO.lines;
say "Part 1:";
put part1(@data);
say "Part 2:";
put part2(@data);
