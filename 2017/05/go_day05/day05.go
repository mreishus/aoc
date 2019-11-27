// Package main provides ...

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func AddOne(x int) int {
	return x + 1
}

// Parse filename -> slice of ints
func Parse(filename string) []int {
	ints := make([]int, 0)

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		i, err := strconv.Atoi(line)
		if err != nil {
			log.Fatal(err)
		}
		ints = append(ints, i)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return ints
}

func Part1(jumps []int) int {
	current_idx := 0
	old_idx := 0
	steps := 0
	max := len(jumps)
	for {
		// Save old
		old_idx = current_idx

		// Are we done?
		if current_idx >= max {
			break
		}

		// Jump
		current_jump := jumps[current_idx]
		current_idx += current_jump

		// Increment old by one
		jumps[old_idx] += 1
		steps += 1
	}
	return steps
}

func Part2(jumps []int) int {
	current_idx := 0
	old_idx := 0
	steps := 0
	max := len(jumps)
	for {
		// Save old
		old_idx = current_idx

		// Are we done?
		if current_idx >= max {
			// fmt.Println(jumps)
			break
		}

		// Jump
		current_jump := jumps[current_idx]
		current_idx += current_jump

		// Increment old by one
		if jumps[old_idx] >= 3 {
			jumps[old_idx] -= 1
		} else {
			jumps[old_idx] += 1
		}
		steps += 1
	}
	return steps
}

func main() {
	jumps := Parse("../input.txt")
	fmt.Println("Part1:")
	// fmt.Println(jumps)
	steps := Part1(jumps)
	fmt.Println(steps)

	fmt.Println("Part2:")
	jumps = Parse("../input.txt")
	// fmt.Println(jumps)
	// 3220: Incorrect guess, answer is too low.
	steps = Part2(jumps)
	fmt.Println(steps)
}
