// Package main provides ...
package main

import "testing"

func TestPart1(t *testing.T) {
	t.Run("It calculates Part1", func(t *testing.T) {
		elves := Parse("../../inputs/01/input.txt")
		got := PartOne(elves)
		want := 69912
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
func TestPart2(t *testing.T) {
	t.Run("It calculates Part2", func(t *testing.T) {
		elves := Parse("../../inputs/01/input.txt")
		got := PartTwo(elves)
		want := 208180
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
