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

func ApplyCommandsMultiple(times int, positions_in []int, swaps_in map[string]string, commands []Command) ([]int, map[string]string) {
	// Copy positions_in -> positions
	positions := make([]int, len(positions_in))
	copy(positions, positions_in)

	// Copy swaps_in -> swaps
	swaps := make(map[string]string, len(swaps_in))
	for key, value := range swaps_in {
		swaps[key] = value
	}

	positions_for_step := make(map[int][]int, 0)
	swaps_for_step := make(map[int]map[string]string, 0)
	i := 1
	positions_for_step[1] = positions
	swaps_for_step[1] = swaps

	for i < times {
		// fmt.Println(i)
		if i*2 < times {
			// Able to double
			// fmt.Println("Double")
			positions, swaps = Compose(positions, swaps, positions, swaps)
			i *= 2
		} else {
			// Can't double, find the largest number we've already computed to add
			gap := times - i
			next_step := 1
			for k, _ := range positions_for_step {
				if k > next_step && k <= gap {
					next_step = k
				}
			}
			// fmt.Printf("--> %v\n", next_step)
			positions, swaps = Compose(positions, swaps, positions_for_step[next_step], swaps_for_step[next_step])
			i += next_step
		}
		positions_for_step[i] = positions
		swaps_for_step[i] = swaps
	}
	return positions, swaps
}

func Compose(positions_in1 []int, swaps_in1 map[string]string, positions_in2 []int, swaps_in2 map[string]string) ([]int, map[string]string) {
	positions := make([]int, len(positions_in1))
	swaps := make(map[string]string, len(swaps_in1))

	// Positions 1 [5, 4, 3, 2, 1, 0]
	// Positions 2 [0, 2, 1, 3, 4, 5]
	// Compose these. Use the values in 2 as indexes to look up 1
	for i, _ := range positions_in1 {
		val2 := positions_in2[i]
		positions[i] = positions_in1[val2]
	}

	// Swaps 1 { "a": "a", "b": "c", "c": "b", "d": "d" }
	// Swaps 2 { "a": "a", "b": "b", "c": "d", "d": "c" }
	for key1, value1 := range swaps_in1 {
		swaps[key1] = swaps_in2[value1]
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

func Part2(length int, commands []Command) string {
	positions, swaps := Init(length)
	positions, swaps = ApplyCommands(positions, swaps, commands)
	positions, swaps = ApplyCommandsMultiple(1_000_000_000, positions, swaps, commands)
	return FinalPositions(length, positions, swaps)
}

func main() {
	// Test
	commands := Parse("../input_small.txt")
	final := Part1(5, commands)
	fmt.Println("Part 1 Example:")
	fmt.Println(final)
	fmt.Println("Part 2 Example:")
	fmt.Println(Part2(5, commands))

	fmt.Println("")

	// Part 1
	commands = Parse("../input.txt")
	final = Part1(16, commands)
	fmt.Println("Part 1:")
	fmt.Println(final)
	fmt.Println("Part 2:")
	fmt.Println(Part2(16, commands))
}
