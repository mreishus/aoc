// Package main provides ...
package main

import "testing"

func TestPart1(t *testing.T) {
	t.Run("Works on small input", func(t *testing.T) {
		spreadSheet := Parse("../input_small.txt")
		got := Part1(spreadSheet)
		want := 18
		if got != want {
			t.Errorf("got %v want %v", got, want)
		}
	})
}
func TestPart2(t *testing.T) {
	t.Run("DivChecksum works 1", func(t *testing.T) {
		input := []int{5, 9, 2, 8}
		got, err := DivChecksum(input)
		want := 4
		AssertDivChecksum(t, got, want, err)
	})
	t.Run("DivChecksum works 2", func(t *testing.T) {
		input := []int{9, 4, 7, 3}
		got, err := DivChecksum(input)
		want := 3
		AssertDivChecksum(t, got, want, err)
	})
	t.Run("DivChecksum works 3", func(t *testing.T) {
		input := []int{3, 8, 6, 5}
		got, err := DivChecksum(input)
		want := 2
		AssertDivChecksum(t, got, want, err)
	})
	t.Run("Part2 works", func(t *testing.T) {
		spreadSheet := Parse("../input_small2.txt")
		got := Part2(spreadSheet)
		want := 9
		if got != want {
			t.Errorf("got %v want %v", got, want)
		}
	})
}
func AssertDivChecksum(t *testing.T, got, want int, err error) {
	t.Helper()
	if got != want {
		t.Errorf("got %v want %v", got, want)
	}
	if err != nil {
		t.Errorf("got an error, didn't want one")
	}
}
