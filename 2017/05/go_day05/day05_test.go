// Package main provides ...
package main

import (
	"reflect"
	"testing"
)

func TestAddOne(t *testing.T) {
	t.Run("It can parse small_input.txt", func(t *testing.T) {
		got := Parse("../input_small.txt")
		want := []int{0, 3, 0, 1, -3}
		if !reflect.DeepEqual(got, want) {
			t.Errorf("got %v want %v", got, want)
		}
	})
	t.Run("Part1 on small_input.txt", func(t *testing.T) {
		jumps := Parse("../input_small.txt")
		steps := Part1(jumps)
		got := steps
		want := 5
		if steps != want {
			t.Errorf("got %v want %v", got, want)
		}
	})
	t.Run("Part2 on small_input.txt", func(t *testing.T) {
		jumps := Parse("../input_small.txt")
		steps := Part2(jumps)
		got := steps
		want := 10
		if steps != want {
			t.Errorf("got %v want %v", got, want)
		}
	})

}
