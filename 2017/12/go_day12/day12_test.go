// Package main provides ...
package main

import "testing"

func TestPartOne(t *testing.T) {
	t.Run("Correct P1 Example", func(t *testing.T) {
		rules := Parse("../input_small.txt")
		groupings := BuildGroupings(rules)
		got := Part1(groupings)
		want := 6
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
	t.Run("Correct P1 Answer", func(t *testing.T) {
		rules := Parse("../input.txt")
		groupings := BuildGroupings(rules)
		got := Part1(groupings)
		want := 239
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}

func TestPartTwo(t *testing.T) {
	t.Run("Correct P2 Example", func(t *testing.T) {
		rules := Parse("../input_small.txt")
		groupings := BuildGroupings(rules)
		got := Part2(groupings)
		want := 2
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
	t.Run("Correct P2 Answer", func(t *testing.T) {
		rules := Parse("../input.txt")
		groupings := BuildGroupings(rules)
		got := Part2(groupings)
		want := 215
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
