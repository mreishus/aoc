// Package main provides ...
package main

import "testing"

func TestDay01(t *testing.T) {
	tests := []struct {
		inputStr  string
		outputInt int
	}{
		{"1122", 3},
		{"1111", 4},
		{"1234", 0},
		{"91212129", 9},
	}

	for _, test := range tests {
		t.Run(test.inputStr, func(t *testing.T) {
			got := Part1(test.inputStr)
			want := test.outputInt
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func TestDay02(t *testing.T) {
	tests := []struct {
		inputStr  string
		outputInt int
	}{
		{"1212", 6},
		{"1221", 0},
		{"123425", 4},
		{"123123", 12},
		{"12131415", 4},
	}

	for _, test := range tests {
		t.Run(test.inputStr, func(t *testing.T) {
			got := Part2(test.inputStr)
			want := test.outputInt
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func TestRotate(t *testing.T) {
	t.Run("Rotate by one", func(t *testing.T) {
		got := Rotate("hello", 1)
		want := "elloh"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
	t.Run("Rotate by zero", func(t *testing.T) {
		got := Rotate("hello", 0)
		want := "hello"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
	t.Run("Rotate by half", func(t *testing.T) {
		got := Rotate("abc123", 3)
		want := "123abc"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
	t.Run("Rotate by full", func(t *testing.T) {
		got := Rotate("abc123", 6)
		want := "abc123"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
	t.Run("Rotate by double", func(t *testing.T) {
		got := Rotate("abc123", 12)
		want := "abc123"
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}
func TestAddOne(t *testing.T) {
	// t.Run("It adds one", func(t *testing.T) {
	// 	got := AddOne(1)
	// 	want := 2
	// 	if got != want {
	// 		t.Errorf("got %q want %q", got, want)
	// 	}
	// })
}
