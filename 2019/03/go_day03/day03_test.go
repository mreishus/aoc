// Package main provides ...
package main

import "testing"

func TestScratch(t *testing.T) {
	got := "adsf"
	want := "asdf"
	if got != want {
		t.Errorf("scratch: got %v want %v", got, want)
	}
}
