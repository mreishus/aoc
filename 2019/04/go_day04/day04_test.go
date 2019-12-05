// Package main provides ...
package main

import (
	"strconv"
	"testing"
)

func TestSolve(t *testing.T) {
	t.Run("It works", func(t *testing.T) {
		got := Solve(200000, 300000)
		want := 771
		if got != want {
			t.Errorf("got %v want %v", got, want)
		}
	})
}
func TestSolve2(t *testing.T) {
	t.Run("It works", func(t *testing.T) {
		got := Solve2(200000, 300000)
		want := 546
		if got != want {
			t.Errorf("got %v want %v", got, want)
		}
	})
}

func TestIsPassword(t *testing.T) {
	tests := []struct {
		input  int
		output bool
	}{
		{111111, true},
		{223450, false},
		{123789, false},
		{123444, true},
	}

	for _, test := range tests {
		name := strconv.Itoa(test.input)
		t.Run(name, func(t *testing.T) {
			want := test.output
			got := IsPassword(test.input)
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func TestIsPassword2(t *testing.T) {
	tests := []struct {
		input  int
		output bool
	}{
		{111111, false},
		{223450, false},
		{123789, false},
		{123444, false},
		{112233, true},
		{123444, false},
		{111122, true},
		{111123, false},
	}

	for _, test := range tests {
		name := strconv.Itoa(test.input)
		t.Run(name, func(t *testing.T) {
			want := test.output
			got := IsPassword2(test.input)
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}
