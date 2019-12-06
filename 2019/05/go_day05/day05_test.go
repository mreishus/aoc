// Package main provides ...
package main

import (
	"reflect"
	"testing"
)

func TestDigitFromRight(t *testing.T) {
	tests := []struct {
		num      int
		i        int
		expected int
	}{
		{12345, 0, 5},
		{12345, 1, 4},
		{12345, 2, 3},
		{12345, 3, 2},
		{12345, 4, 1},
		{12345, 5, 0},
		{498, 0, 8},
		{498, 1, 9},
		{498, 2, 4},
		{498, 3, 0},
		{498, 4, 0},
		{498, 5, 0},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := DigitFromRight(test.num, test.i)
			want := test.expected
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func Test81(t *testing.T) {
	program := []int{3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{7}, []int{0}},
		{[]int{8}, []int{1}},
		{[]int{9}, []int{0}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func Test82(t *testing.T) {
	program := []int{3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{7}, []int{1}},
		{[]int{8}, []int{0}},
		{[]int{9}, []int{0}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func Test83(t *testing.T) {
	program := []int{3, 3, 1108, -1, 8, 3, 4, 3, 99}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{7}, []int{0}},
		{[]int{8}, []int{1}},
		{[]int{9}, []int{0}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func Test84(t *testing.T) {
	program := []int{3, 3, 1107, -1, 8, 3, 4, 3, 99}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{7}, []int{1}},
		{[]int{8}, []int{0}},
		{[]int{9}, []int{0}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func TestJump1(t *testing.T) {
	program := []int{3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{0}, []int{0}},
		{[]int{10}, []int{1}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func TestJump2(t *testing.T) {
	program := []int{3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{0}, []int{0}},
		{[]int{10}, []int{1}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

func TestLonger(t *testing.T) {
	program := []int{3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99}
	tests := []struct {
		inputs []int
		want   []int
	}{
		{[]int{2}, []int{999}},
		{[]int{8}, []int{1000}},
		{[]int{12}, []int{1001}},
	}

	for _, test := range tests {
		t.Run("whatever", func(t *testing.T) {
			got := Solve(program, test.inputs)
			want := test.want
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}
