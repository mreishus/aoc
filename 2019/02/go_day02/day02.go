// Package main provides ...
package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

var (
	OP_ADD  = 1
	OP_MULT = 2
	OP_STOP = 99
)

func Parse(filename string) []int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	var strNums []string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		strNums = strings.Split(line, ",")
		break
	}

	nums := make([]int, 0)
	for _, thisStrNum := range strNums {
		thisNum, err := strconv.Atoi(strings.TrimSpace(thisStrNum))
		if err != nil {
			log.Fatal(err)
		}
		nums = append(nums, thisNum)
	}

	return nums
}

func Compute(program []int) []int {
	i := 0
	isRunning := true
	for isRunning {
		instruction := program[i]
		switch instruction {
		case OP_ADD:
			// fmt.Println("add")
			posIn1 := program[i+1]
			posIn2 := program[i+2]
			posOut := program[i+3]
			program[posOut] = program[posIn1] + program[posIn2]
			i += 4
		case OP_MULT:
			// fmt.Println("multiply")
			posIn1 := program[i+1]
			posIn2 := program[i+2]
			posOut := program[i+3]
			program[posOut] = program[posIn1] * program[posIn2]
			i += 4
		case OP_STOP:
			isRunning = false
		default:
			log.Fatal("Unknown Instruction")
		}
	}
	return program
}

func Part1(program []int) int {
	program = CloneProgram(program)
	program[1] = 12
	program[2] = 2
	program = Compute(program)
	return program[0]
}

func Part2(program []int) int {
	for i := 0; i < 100; i++ {
		for j := 0; j < 100; j++ {
			if Part2Eval(program, i, j) == 19690720 {
				return Part2Answer(i, j)
			}
		}
	}
	return 0
}

func Part2Eval(program []int, noun int, verb int) int {
	program = CloneProgram(program)
	program[1] = noun
	program[2] = verb
	program = Compute(program)
	return program[0]
}

func Part2Answer(noun int, verb int) int {
	return 100*noun + verb
}

func CloneProgram(program []int) []int {
	x := make([]int, len(program))
	copy(x, program)
	return x
}

func main() {
	nums := Parse("../input.txt")
	fmt.Println("AOC 2019 Day 02:")
	fmt.Println("Part 1:")
	fmt.Println(Part1(nums))
	fmt.Println("Part2:")
	fmt.Println(Part2(nums))
}
