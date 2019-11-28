// Package main provides ...
package main

import "testing"

func TestGetBottomNode(t *testing.T) {
	t.Run("works", func(t *testing.T) {
		nodes := Parse("../input_small.txt")
		node := GetBottomNode(nodes)
		got := node.Name
		want := "tknk"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
