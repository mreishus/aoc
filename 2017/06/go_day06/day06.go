// Package main provides ...
package main

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// Redistribute finds the memory bank with the most blocks (ties won by
// the lowest-numbered memory bank) and redistributes those blocks among the
// banks. To do this, it removes all of the blocks from the selected bank, then
// moves to the next (by index) memory bank and inserts one of the blocks. It
// continues doing this until it runs out of blocks; if it reaches the last
// memory bank, it wraps around to the first one.
func Redistribute(banks []int) []int {
	maxI, maxV := max(banks)
	banks[maxI] = 0

	i := maxI
	l := len(banks)
	for maxV > 0 {
		i = (i + 1) % l
		banks[i]++
		maxV--
	}

	return banks
}

func max(list []int) (int, int) {
	max := 0
	maxIndex := 0
	for i, item := range list {
		if item > max {
			max = item
			maxIndex = i
		}
	}
	return maxIndex, max
}

// Part1 solves part 1
func Part1(banks []int) int {
	seen := make(map[[32]byte]int)
	seen[sliceHash(banks)] = 1
	steps := 0

	for {
		// Compute new bank
		steps++
		banks = Redistribute(banks)
		hash := sliceHash(banks)

		// Check for seen
		if seen[hash] == 1 {
			break
		}

		// Record seen
		seen[hash] = 1
	}
	return steps

	// fmt.Printf("%v", banks)
	// banks = Redistribute(banks)
	// fmt.Printf("%v", banks)
	// banks = Redistribute(banks)
	// fmt.Printf("%v", banks)
}

func sliceHash(list []int) [32]byte {
	delim := " "
	var buffer bytes.Buffer
	for i := range list {
		buffer.WriteString(strconv.Itoa(list[i]))
		buffer.WriteString(delim)
	}
	return (sha256.Sum256([]byte(buffer.String())))
}

func Parse(filename string) []int {
	b, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Print(err)
	}

	nums := strings.Fields(string(b))
	banks := make([]int, 0)
	for _, num := range nums {
		n, err := strconv.Atoi(num)
		if err != nil {
			fmt.Print(err)
		}
		banks = append(banks, n)
	}

	return banks
}

func main() {
	// banks := []int{0, 2, 7, 0}
	// fmt.Println(Part1(banks))
	banks := Parse("../input.txt")
	fmt.Println(Part1(banks))
}
