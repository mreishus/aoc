// Package main provides ...
package main

import "testing"

func TestGetLeftNode(t *testing.T) {
	t.Run("works", func(t *testing.T) {
		nodes := Parse("../input_small.txt")
		node := GetLeftNode(nodes)
		got := node.Name
		want := "tknk"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
