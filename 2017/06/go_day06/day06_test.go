// Package main provides ...
package main

import (
	"reflect"
	"testing"
)

func TestRedistrib(t *testing.T) {
	t.Run("works", func(t *testing.T) {
		banks := []int{0, 2, 7, 0}
		got := Redistribute(banks)
		want := []int{2, 4, 1, 2}
		if !reflect.DeepEqual(got, want) {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
func TestPart1(t *testing.T) {
	t.Run("works", func(t *testing.T) {
		banks := []int{0, 2, 7, 0}
		got, _ := Part1(banks)
		want := 5
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
func TestPart2(t *testing.T) {
	t.Run("works", func(t *testing.T) {
		banks := []int{0, 2, 7, 0}
		got := Part2(banks)
		want := 4
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
