package main

import "testing"

func TestAddOne(t *testing.T) {
	t.Run("It adds one", func(t *testing.T) {
		got := AddOne(1)
		want := 2
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
