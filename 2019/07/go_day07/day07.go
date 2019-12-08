// Package main provides ...
package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"strconv"
	"strings"
)

var (
	MODE_POSITION    = 0
	MODE_IMMEDIATE   = 1
	OP_ADD           = 1
	OP_MULT          = 2
	OP_SAVE          = 3
	OP_WRITE         = 4
	OP_JUMP_IF_TRUE  = 5
	OP_JUMP_IF_FALSE = 6
	OP_LESS_THAN     = 7
	OP_EQUALS        = 8
	OP_STOP          = 99
)

type Computer struct {
	Memory          []int
	Inputs          []int
	Outputs         []int
	PC              int
	Halted          bool
	WaitingForInput bool
}

func DigitFromRight(x, n int) int {
	tens := int(math.Pow(10, float64(n)))
	return x / tens % 10
}

// Solve takes a program and inputs, makes a computer, runs it and gets the output
func Solve(program []int, inputs []int) []int {
	c := NewComputer(program, inputs)
	c.Execute()
	return c.Outputs
}

// NewComputer initializes a new computer, given a program to run and inputs
func NewComputer(program []int, inputs []int) Computer {
	memory := make([]int, len(program))
	copy(memory, program)

	myInputs := make([]int, len(inputs))
	copy(myInputs, inputs)

	c := Computer{Memory: memory, Inputs: inputs, PC: 0}
	return c
}

// Direct gets the direct value of the memory address of the Nth arg, or PC + N
func (c Computer) Direct(n int) int {
	return c.Memory[c.PC+n]
}

// Lookup gets the dereferenced value of the Nth arg, after checking the Nth
// mode of the current instruction.
func (c Computer) Lookup(n int) int {
	instruction := c.Memory[c.PC]
	// If instruction is 105, and n=1, mode is the "1", or the 2nd digit
	// from right 0 indexed (3rd when counting naturally)
	mode := DigitFromRight(instruction, n+1)
	if mode == MODE_POSITION {
		return c.Memory[c.Direct(n)]
	} else if mode == MODE_IMMEDIATE {
		return c.Direct(n)
	} else {
		log.Fatal("Unknown mode")
	}
	return 0
}

// AddInput adds an input to a computer
func (c *Computer) AddInput(newInput int) {
	c.Inputs = append(c.Inputs, newInput)
}

// PopOutput returns the oldest output, and removes it from the computer's output
func (c *Computer) PopOutput() (int, error) {
	if len(c.Outputs) == 0 {
		return 0, errors.New("Computer has no output, can't pop")
	}
	first, rest := c.Outputs[0], c.Outputs[1:]
	c.Outputs = rest
	return first, nil
}

// Execute runs instructions until the computer stops (99) or pauses (Waiting for input)
func (c *Computer) Execute() {
	// Stopped: c.Halted == true || (c.WaitingForInput && len(c.Inputs) == 0)
	// Running is inverse
	for c.Halted == false && (!c.WaitingForInput || len(c.Inputs) > 0) {
		c.Step()
	}
}

// Step executes the next instruction and moves the PC
func (c *Computer) Step() {
	instruction := c.Memory[c.PC] % 100
	if instruction == OP_ADD {
		c.Memory[c.Direct(3)] = c.Lookup(1) + c.Lookup(2)
		c.PC += 4
	} else if instruction == OP_MULT {
		c.Memory[c.Direct(3)] = c.Lookup(1) * c.Lookup(2)
		c.PC += 4
	} else if instruction == OP_SAVE {
		if len(c.Inputs) == 0 {
			// No input available, pause execution
			c.WaitingForInput = true
		} else {
			// Process Input
			c.WaitingForInput = false
			input := c.Inputs[0]
			c.Inputs = c.Inputs[1:]
			c.Memory[c.Direct(1)] = input
			c.PC += 2
		}
	} else if instruction == OP_WRITE {
		c.Outputs = append(c.Outputs, c.Lookup(1))
		c.PC += 2
	} else if instruction == OP_JUMP_IF_TRUE {
		if c.Lookup(1) != 0 {
			c.PC = c.Lookup(2)
		} else {
			c.PC += 3
		}
	} else if instruction == OP_JUMP_IF_FALSE {
		if c.Lookup(1) == 0 {
			c.PC = c.Lookup(2)
		} else {
			c.PC += 3
		}
	} else if instruction == OP_LESS_THAN {
		if c.Lookup(1) < c.Lookup(2) {
			c.Memory[c.Direct(3)] = 1
		} else {
			c.Memory[c.Direct(3)] = 0
		}
		c.PC += 4
	} else if instruction == OP_EQUALS {
		if c.Lookup(1) == c.Lookup(2) {
			c.Memory[c.Direct(3)] = 1
		} else {
			c.Memory[c.Direct(3)] = 0
		}
		c.PC += 4
	} else if instruction == OP_STOP {
		c.Halted = true
	}
}

// Returns (Seq, Val)
func AmplifyOnceMaxSeq(program []int) ([]int, int) {
	// value = amplify_once(program, phase_sequence)
	// {phase_sequence, value}
	// end)
	// |> Enum.max_by(fn {_phase_sequence, value} ->
	// value
	// end)

	maxValue := 0
	maxSeq := []int{}

	for _, seq := range permutations([]int{0, 1, 2, 3, 4}) {
		value := AmplifyOnce(program, seq)
		if value > maxValue {
			maxValue = value
			maxSeq = seq
		}
	}
	return maxSeq, maxValue
}

func AmplifyOnce(program []int, phaseSeq []int) int {
	computers := make([]Computer, 0)
	for _, num := range phaseSeq {
		c := NewComputer(program, []int{num})
		c.Execute()
		computers = append(computers, c)
	}

	lastOutput := 0
	var err error
	for _, c := range computers {
		c.AddInput(lastOutput)
		c.Execute()
		lastOutput, err = c.PopOutput()
		if err != nil {
			log.Fatal("AmplifyOnce: Couldn't read output")
		}
	}
	return lastOutput
}

func Parse(filename string) []int {
	program := make([]int, 0)

	b, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	s := string(b)
	sList := strings.Split(strings.TrimSpace(s), ",")
	for _, sNum := range sList {
		num, err := strconv.Atoi(sNum)
		if err != nil {
			log.Fatal(err)
		}
		program = append(program, num)
	}
	return program
}

// https://stackoverflow.com/questions/30226438/generate-all-permutations-in-go
func permutations(arr []int) [][]int {
	var helper func([]int, int)
	res := [][]int{}

	helper = func(arr []int, n int) {
		if n == 1 {
			tmp := make([]int, len(arr))
			copy(tmp, arr)
			res = append(res, tmp)
		} else {
			for i := 0; i < n; i++ {
				helper(arr, n-1)
				if n%2 == 1 {
					tmp := arr[i]
					arr[i] = arr[n-1]
					arr[n-1] = tmp
				} else {
					tmp := arr[0]
					arr[0] = arr[n-1]
					arr[n-1] = tmp
				}
			}
		}
	}
	helper(arr, len(arr))
	return res
}

func main() {
	fmt.Println("Hello, world")
	program := Parse("../input.txt")
	p1MaxSeq, p1MaxValue := AmplifyOnceMaxSeq(program)
	fmt.Println("Part 1:")
	fmt.Println(p1MaxSeq)
	fmt.Println(p1MaxValue)
	// output2 := Solve(program, []int{5})
	// fmt.Println("Part 2:")
	// fmt.Println(output2)
}
