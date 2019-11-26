// Package main provides ...
package main

import "testing"

func TestPart1(t *testing.T) {
	t.Run("Works on small input", func(t *testing.T) {
		spreadSheet := Parse("../input_small.txt")
		got := Part1(spreadSheet)
		want := 18
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
