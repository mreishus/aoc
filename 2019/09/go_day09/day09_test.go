// Package main provides ...
package main

import (
	"reflect"
	"testing"
)

func TestDay9Part1(t *testing.T) {
	program := Parse("../../09/input.txt")
	got := Solve(program, []int{1})
	want := []int{3780860499}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("got %v want %v", got, want)
	}
}

func TestDay9Part2(t *testing.T) {
	program := Parse("../../09/input.txt")
	got := Solve(program, []int{2})
	want := []int{33343}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("got %v want %v", got, want)
	}
}

func TestDay9TestProgs(t *testing.T) {
	quineProg := []int{109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99}

	tests := []struct {
		name   string
		prog   []int
		output []int
	}{
		{
			name:   "day 9 test 1",
			prog:   quineProg,
			output: quineProg,
		},
		{
			name:   "day 9 test 2",
			prog:   []int{1102, 34915192, 34915192, 7, 4, 7, 99, 0},
			output: []int{1219070632396864},
		},
		{
			name:   "day 9 test 3",
			prog:   []int{104, 1125899906842624, 99},
			output: []int{1125899906842624},
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got := Solve(test.prog, []int{})
			want := test.output
			if !reflect.DeepEqual(got, want) {
				t.Errorf("got %v want %v", got, want)
			}
		})
	}
}

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

func TestDay7Part1(t *testing.T) {
	program := Parse("../../07/input.txt")
	p1MaxSeq, p1MaxVal := AmplifyOnceMaxSeq(program)
	wantMaxSeq := []int{2, 0, 3, 1, 4}
	wantMaxVal := 13848
	if !reflect.DeepEqual(p1MaxSeq, wantMaxSeq) {
		t.Errorf("got %v want %v", p1MaxSeq, wantMaxSeq)
	}
	if p1MaxVal != wantMaxVal {
		t.Errorf("got %v want %v", p1MaxVal, wantMaxVal)
	}
}
func TestDay7Part2(t *testing.T) {
	program := Parse("../../07/input.txt")
	p2MaxSeq, p2MaxVal := AmplifyLoopMaxSeq(program)
	wantMaxSeq := []int{6, 8, 7, 5, 9}
	wantMaxVal := 12932154
	if !reflect.DeepEqual(p2MaxSeq, wantMaxSeq) {
		t.Errorf("got %v want %v", p2MaxSeq, wantMaxSeq)
	}
	if p2MaxVal != wantMaxVal {
		t.Errorf("got %v want %v", p2MaxVal, wantMaxVal)
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

func TestAmplifyLoop(t *testing.T) {
	progB1 := []int{3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5}
	progB2 := []int{3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10}

	tests := []struct {
		name     string
		prog     []int
		phaseSeq []int
		wantVal  int
	}{
		{
			"B1", progB1, []int{9, 8, 7, 6, 5}, 139629729,
		},
		{
			"B2", progB2, []int{9, 7, 8, 5, 6}, 18216,
		},
	}

	for _, test := range tests {
		// First: Check the correct answer with AmplifyOnce
		t.Run(test.name+" T1", func(t *testing.T) {
			got := AmplifyLoop(test.prog, test.phaseSeq)
			want := test.wantVal
			if got != want {
				t.Errorf("got %v want %v", got, want)
			}
		})
		// Second: See if we can generate the correct answer with AmplifyOnceMaxSeq
		t.Run(test.name+" T1", func(t *testing.T) {
			gotSeq, gotVal := AmplifyLoopMaxSeq(test.prog)
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
