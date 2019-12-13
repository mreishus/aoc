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
	MODE_POSITION        = 0
	MODE_IMMEDIATE       = 1
	MODE_RELATIVE        = 2
	OP_ADD               = 1
	OP_MULT              = 2
	OP_SAVE              = 3
	OP_WRITE             = 4
	OP_JUMP_IF_TRUE      = 5
	OP_JUMP_IF_FALSE     = 6
	OP_LESS_THAN         = 7
	OP_EQUALS            = 8
	OP_SET_RELATIVE_BASE = 9
	OP_STOP              = 99
)

type Computer struct {
	Memory          []int
	Inputs          []int
	Outputs         []int
	PC              int
	RelativeBase    int
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
	// memory := make([]int, len(program))
	// copy(memory, program)

	// Unsure if this approach works
	memory := make([]int, len(program)+10000)
	copy(memory, program)

	myInputs := make([]int, len(inputs))
	copy(myInputs, inputs)

	c := Computer{Memory: memory, Inputs: inputs, PC: 0, RelativeBase: 0}
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
	} else if mode == MODE_RELATIVE {
		address := c.Direct(n) + c.RelativeBase
		return c.Memory[address]
	} else {
		log.Fatal("Unknown mode")
	}
	return 0
}

func (c Computer) LookupLeft(n int) int {
	// Now: LookupLeft is same as direct
	instruction := c.Memory[c.PC]
	mode := DigitFromRight(instruction, n+1)
	if mode == MODE_POSITION {
		return c.Direct(n)
	} else if mode == MODE_IMMEDIATE {
		return c.Direct(n)
	} else if mode == MODE_RELATIVE {
		address := c.Direct(n) + c.RelativeBase
		return address
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
		c.Memory[c.LookupLeft(3)] = c.Lookup(1) + c.Lookup(2)
		c.PC += 4
	} else if instruction == OP_MULT {
		c.Memory[c.LookupLeft(3)] = c.Lookup(1) * c.Lookup(2)
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
			c.Memory[c.LookupLeft(1)] = input
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
			c.Memory[c.LookupLeft(3)] = 1
		} else {
			c.Memory[c.LookupLeft(3)] = 0
		}
		c.PC += 4
	} else if instruction == OP_EQUALS {
		if c.Lookup(1) == c.Lookup(2) {
			c.Memory[c.LookupLeft(3)] = 1
		} else {
			c.Memory[c.LookupLeft(3)] = 0
		}
		c.PC += 4
	} else if instruction == OP_SET_RELATIVE_BASE {
		c.RelativeBase += c.Lookup(1)
		c.PC += 2
	} else if instruction == OP_STOP {
		c.Halted = true
	} else {
		log.Fatalf("Unknown instruction %v", instruction)
	}
}

// AmplifyOnceMaxSeq takes a program given, and runs
// AmplifyOnce with many different 'phase sequence' values,
// (all permutations of (01234)).  It finds the sequence
// that returns the highest value, then returns both the
// sequence and the value.
func AmplifyOnceMaxSeq(program []int) ([]int, int) {
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

// AmplifyOnce sets up a chain of 5 computers, loads them with a program,
// initializes them with the "Phase Sequence" values, sends a 0 to the first
// computer, sends the first computer's output to the second computer, etc,
// then returns the last computer's output.
func AmplifyOnce(program []int, phaseSeq []int) int {
	computers := make([]*Computer, 0)
	for _, num := range phaseSeq {
		c := NewComputer(program, []int{num})
		c.Execute()
		computers = append(computers, &c)
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

// AmplifyLoopMaxSeq takes a program given, and runs
// AmplifyLoop with many different 'phase sequence' values,
// (all permutations of (56789)).  It finds the sequence
// that returns the highest value, then returns both the
// sequence and the value.
func AmplifyLoopMaxSeq(program []int) ([]int, int) {
	maxValue := 0
	maxSeq := []int{}

	for _, seq := range permutations([]int{5, 6, 7, 8, 9}) {
		value := AmplifyLoop(program, seq)
		if value > maxValue {
			maxValue = value
			maxSeq = seq
		}
	}
	return maxSeq, maxValue
}

// AmplifyLoop sets up a chain of 5 computers, loads them with a program,
// initializes them with the "Phase Sequence" values, sends a 0 to the first
// computer, sends the first computer's output to the second computer, etc.
// The last computer's output is fed to the first computer's input in a feedback
// loop.  The signal keeps looping until at least one of the computers has halted,
// then it finishes the current cycle and returns the last computer's output.
func AmplifyLoop(program []int, phaseSeq []int) int {
	computers := make([]*Computer, 0)
	for _, num := range phaseSeq {
		c := NewComputer(program, []int{num})
		c.Execute()
		computers = append(computers, &c)
	}

	lastOutput := 0
	var err error
	stillRunning := true

	for stillRunning && lastOutput >= 0 {
		for _, c := range computers {
			c.AddInput(lastOutput)
			c.Execute()
			lastOutput, err = c.PopOutput()
			if err != nil {
				log.Fatal("AmplifyLoop: Couldn't read output")
			}
			if c.Halted {
				stillRunning = false
			}
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

///////// PREVIOUS INTCODE END //////////////

type Coord struct {
	X, Y int
}

// Move moves a coordinate by one step in the specified direction.
func Move(where Coord, direction string) Coord {
	switch direction {
	case "R":
		return Coord{where.X + 1, where.Y}
	case "L":
		return Coord{where.X - 1, where.Y}
	case "U":
		return Coord{where.X, where.Y - 1}
	case "D":
		return Coord{where.X, where.Y + 1}
	}
	log.Fatal("Move: Unknown direction")
	return where
}

func TurnRight(direction string) string {
	switch direction {
	case "U":
		return "R"
	case "R":
		return "D"
	case "D":
		return "L"
	case "L":
		return "U"
	}
	log.Fatal("TurnRight: Unknown direction")
	return "Z"
}

func TurnLeft(direction string) string {
	switch direction {
	case "U":
		return "L"
	case "L":
		return "D"
	case "D":
		return "R"
	case "R":
		return "U"
	}
	log.Fatal("TurnLeft: Unknown direction")
	return "Z"
}

func PainterRobot(program []int, initialColor int) map[Coord]int {
	c := NewComputer(program, []int{})
	grid := make(map[Coord]int, 0)

	location := Coord{0, 0}
	direction := "U"
	grid[location] = initialColor

	for {
		currentSquare := grid[location]
		c.AddInput(currentSquare)
		c.Execute()
		if c.Halted {
			break
		}
		paintColor, err := c.PopOutput()
		if err != nil {
			log.Fatal("PainterRobot: Couldn't read paintColor")
		}
		turnDir, err := c.PopOutput()
		if err != nil {
			log.Fatal("PainterRobot: Couldn't read turnDir")
		}
		grid[location] = paintColor
		if turnDir == 1 {
			direction = TurnRight(direction)
		} else if turnDir == 0 {
			direction = TurnLeft(direction)
		} else {
			log.Fatal("Told to turn an incorrect direction")
		}
		location = Move(location, direction)
	}

	return grid
}

func NumPaintedSquares(grid map[Coord]int) int {
	i := 0
	for range grid {
		i++
	}
	return i
}

func DisplayGrid(grid map[Coord]int) {
	// for y in range(-3, 7):
	//     for x in range(-5, 45):
	for y := -1; y < 7; y++ {
		for x := -5; x < 45; x++ {
			value := grid[Coord{x, y}]
			if value == 1 {
				fmt.Printf("#")
			} else {
				fmt.Printf(" ")
			}
		}
		fmt.Println("")
	}
}

func main() {
	fmt.Println("Advent of Code 2019 Day 9")

	program := Parse("../../11/input.txt")
	grid1 := PainterRobot(program, 0)
	fmt.Println("Part 1:")
	fmt.Println(NumPaintedSquares(grid1))

	grid2 := PainterRobot(program, 1)
	fmt.Println("Part 2:")
	fmt.Println(NumPaintedSquares(grid2))
	DisplayGrid(grid2)
}
