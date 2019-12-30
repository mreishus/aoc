// Package main provides ...
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type Instruction int

const (
	Spin      Instruction = 1
	SwapIndex Instruction = 2
	SwapChar  Instruction = 3
)

type Command struct {
	Inst       Instruction
	SpinAmount int
	SwapIndex0 int
	SwapIndex1 int
	SwapChar0  string
	SwapChar1  string
}

func Parse(filename string) []Command {
	commands := make([]Command, 0)

	b, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	s := string(b)
	sList := strings.Split(strings.TrimSpace(s), ",")
	for _, sCommand := range sList {
		// sInt (examples) "x7/5", "x13/4", "s14", "pc/m"
		first, rest := sCommand[0], sCommand[1:]
		command := Command{}

		if int(first) == int('s') {
			command = ParseSpin(rest)
		} else if int(first) == int('x') {
			command = ParseExchange(rest)
		} else if int(first) == int('p') {
			command = ParsePartner(rest)
		}

		commands = append(commands, command)
	}
	return commands
}

func ParseSpin(rest string) Command {
	// parse "s14"
	num, err := strconv.Atoi(rest)
	if err != nil {
		log.Fatal(err)
	}
	return Command{Inst: Spin, SpinAmount: num}
}

func ParseExchange(rest string) Command {
	// parse "x7/5"
	nums := strings.Split(rest, "/")
	num0, err := strconv.Atoi(nums[0])
	if err != nil {
		log.Fatal(err)
	}
	num1, err := strconv.Atoi(nums[1])
	if err != nil {
		log.Fatal(err)
	}
	return Command{Inst: SwapIndex, SwapIndex0: num0, SwapIndex1: num1}
}

func ParsePartner(rest string) Command {
	// parse "pc/m"
	chars := strings.Split(rest, "/")
	char0 := chars[0]
	char1 := chars[1]
	return Command{Inst: SwapChar, SwapChar0: char0, SwapChar1: char1}
}

/// PARSING END

func Rotate(nums []int, k int) []int {
	if k < 0 || len(nums) == 0 {
		return nums
	}

	r := len(nums) - k%len(nums)
	nums = append(nums[r:], nums[:r]...)

	return nums
}

func Init(size int) ([]int, map[string]string) {
	// If size 5, Start with
	// Positions = [0, 1, 2, 3, 4]
	// Swaps = ["a": "a", "b": "b", ... "e": "e"]
	positions := make([]int, size)
	swaps := make(map[string]string, size)
	for index := 0; index < size; index++ {
		positions[index] = index
		letter := string(rune(97 + index))
		swaps[letter] = letter
	}
	return positions, swaps
}

func ApplyCommands(positions_in []int, swaps_in map[string]string, commands []Command) ([]int, map[string]string) {
	// Copy positions_in -> positions
	positions := make([]int, len(positions_in))
	copy(positions, positions_in)

	// Copy swaps_in -> swaps
	swaps := make(map[string]string, len(swaps_in))
	for key, value := range swaps_in {
		swaps[key] = value
	}

	for _, command := range commands {
		if command.Inst == Spin {
			positions = Rotate(positions, command.SpinAmount)
		} else if command.Inst == SwapIndex {
			i := command.SwapIndex0
			j := command.SwapIndex1
			positions[i], positions[j] = positions[j], positions[i]
		} else if command.Inst == SwapChar {
			i := ""
			j := ""
			for key, value := range swaps {
				if value == command.SwapChar0 {
					i = key
				}
				if value == command.SwapChar1 {
					j = key
				}
			}
			swaps[i], swaps[j] = swaps[j], swaps[i]
		}
	}
	return positions, swaps
}

func FinalPositions(length int, positions []int, swaps map[string]string) string {
	letters := make([]string, length)
	for index := 0; index < length; index++ {
		letter := string(rune(97 + index))
		letters[index] = letter
	}

	final := make([]string, length)
	for i, pos := range positions {
		final[i] = swaps[letters[pos]]
	}

	return strings.Join(final[:], "")
}

func Part1(length int, commands []Command) string {
	positions, swaps := Init(length)
	positions, swaps = ApplyCommands(positions, swaps, commands)
	return FinalPositions(length, positions, swaps)
}

func main() {
	fmt.Println("Hello, world")

	// Test
	commands := Parse("../input_small.txt")
	final := Part1(5, commands)
	fmt.Println(final)

	// Part 1
	commands = Parse("../input.txt")
	final = Part1(16, commands)
	fmt.Println(final)
}
