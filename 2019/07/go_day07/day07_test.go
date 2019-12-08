// Package main provides ...
package main

import (
	"reflect"
	"testing"
)

func TestPauseOnMissingInput(t *testing.T) {
	// Run this program with no inputs
	program := []int{3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8}
	inputs := []int{}
	c := NewComputer(program, inputs)
	c.Execute()
	// C should be waiting for input
	if !c.WaitingForInput {
		t.Errorf("computer not waiting for input")
	}
	// Add input 8 and execute
	c.AddInput(8)
	c.Execute()
	// Should no longer be waiting for input
	if c.WaitingForInput {
		t.Errorf("computer waiting for input inappropriately")
	}
	// Should be halted
	if !c.Halted {
		t.Errorf("computer not halted")
	}
	// Outputs should have 1 in them
	got := c.Outputs
	want := []int{1}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("got %v want %v", got, want)
	}
}

func TestPopOutput(t *testing.T) {
	program := []int{3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8}
	inputs := []int{8}
	c := NewComputer(program, inputs)
	c.Execute()

	oldLen := len(c.Outputs)
	popped, err := c.PopOutput()
	newLen := len(c.Outputs)

	if err != nil {
		t.Errorf("TestPopOutput: didn't expect an error")
	}
	if newLen+1 != oldLen {
		t.Errorf("Popping didn't remove an output")
	}
	if popped != 1 {
		t.Errorf("Incorrect value popped off")
	}
}

func TestAmplifyOnce(t *testing.T) {
	progA1 := []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	progA2 := []int{3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0}
	progA3 := []int{3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0}

	tests := []struct {
		name     string
		prog     []int
		phaseSeq []int
		wantVal  int
	}{
		{
			"A1", progA1, []int{4, 3, 2, 1, 0}, 43210,
		},
		{
			"A2", progA2, []int{0, 1, 2, 3, 4}, 54321,
		},
		{
			"A3", progA3, []int{1, 0, 4, 3, 2}, 65210,
		},
	}

	for _, test := range tests {
		// First: Check the correct answer with AmplifyOnce
		t.Run(test.name+" T1", func(t *testing.T) {
			got := AmplifyOnce(test.prog, test.phaseSeq)
			want := test.wantVal
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
		// Second: See if we can generate the correct answer with AmplifyOnceMaxSeq
		t.Run(test.name+" T1", func(t *testing.T) {
			gotSeq, gotVal := AmplifyOnceMaxSeq(test.prog)
			if !reflect.DeepEqual(gotSeq, test.phaseSeq) {
				t.Errorf("got %v want %v", gotSeq, test.phaseSeq)
			}
			if gotVal != test.wantVal {
				t.Errorf("got %v want %v", gotVal, test.wantVal)
			}
		})
	}
}

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

func TestDay5Part1(t *testing.T) {
	program := Parse("../../05/input.txt")
	got := Solve(program, []int{1})
	want := []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 5821753}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("got %v want %v", got, want)
	}
}

func TestDay5Part2(t *testing.T) {
	program := Parse("../../05/input.txt")
	got := Solve(program, []int{5})
	want := []int{11956381}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("got %v want %v", got, want)
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

func BenchmarkSolve05Part1(b *testing.B) {
	program := Parse("../../05/input.txt")
	for i := 0; i < b.N; i++ {
		Solve(program, []int{1})
	}
}
func BenchmarkSolve05Part2(b *testing.B) {
	program := Parse("../../05/input.txt")
	for i := 0; i < b.N; i++ {
		Solve(program, []int{5})
	}
}
