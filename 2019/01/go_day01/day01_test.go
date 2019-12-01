// Package main provides ...
package main

import "testing"

func TestFuel(t *testing.T) {
	tests := []struct {
		mass  int
		value int
	}{
		{12, 2},
		{14, 2},
		{1969, 654},
		{100756, 33583},
	}

	for _, test := range tests {
		t.Run(string(test.mass), func(t *testing.T) {
			got := Fuel(test.mass)
			want := test.value
			if got != want {
				t.Errorf("fuel: got %v want %v", got, want)
			}

		})
	}
}

func TestTotalFuel(t *testing.T) {
	tests := []struct {
		mass  int
		value int
	}{
		{14, 2},
		{1969, 966},
		{100756, 50346},
	}

	for _, test := range tests {
		t.Run(string(test.mass), func(t *testing.T) {
			got := TotalFuel(test.mass)
			want := test.value
			if got != want {
				t.Errorf("fuel: got %v want %v", got, want)
			}

		})
	}
}
