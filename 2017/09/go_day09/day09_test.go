// Package main provides ...
package main

import "testing"

func TestGroupCount(t *testing.T) {
	tests := []struct {
		name  string
		count int
	}{
		{"{}", 1},
		{"{{{}}}", 3},
		{"{{},{}}", 3},
		{"{{{},{},{{}}}}", 6},
		{"{<{},{},{{}}>}", 1},
		{"{<a>,<a>,<a>,<a>}", 1},
		{"{{<a>},{<a>},{<a>},{<a>}}", 5},
		{"{{<!>},{<!>},{<!>},{<a>}}", 2},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got := GroupCount(test.name)
			want := test.count
			if got != want {
				t.Errorf("[groupcount] got %v want %v input %v", got, want, test.name)
			}
		})
	}
}

func TestGroupScore(t *testing.T) {
	tests := []struct {
		name  string
		score int
	}{

		{"{}", 1},
		{"{{{}}}", 6},
		{"{{},{}}", 5},
		{"{{{},{},{{}}}}", 16},
		{"{<a>,<a>,<a>,<a>}", 1},
		{"{{<ab>},{<ab>},{<ab>},{<ab>}}", 9},
		{"{{<!!>},{<!!>},{<!!>},{<!!>}}", 9},
		{"{{<a!>},{<a!>},{<a!>},{<ab>}}", 3},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got := GroupScore(test.name)
			want := test.score
			if got != want {
				t.Errorf("[groupscore] got %v want %v input %v", got, want, test.name)
			}
		})
	}
}
