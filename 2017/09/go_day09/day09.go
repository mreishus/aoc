// Package main provides ...
package main

import (
	"fmt"
	"io/ioutil"
)

// Process x
func Process(input string) (int, int, int) {
	groupsDeep := 0
	groupCount := 0
	ignoreNext := false
	inGarbage := false
	garbageCount := 0
	score := 0

	for _, s := range input {
		if ignoreNext {
			ignoreNext = false
			continue
		}

		if inGarbage && s != '>' && s != '!' {
			garbageCount += 1
		}

		switch s {
		case '{':
			if !inGarbage {
				groupsDeep++
			}
		case '}':
			if !inGarbage {
				score += groupsDeep
				groupsDeep--
				groupCount++
			}
		case '!':
			ignoreNext = true
		case '<':
			inGarbage = true
		case '>':
			inGarbage = false
		}
	}
	return groupCount, score, garbageCount
}

func ReadFile(filename string) string {
	b, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Print(err)
	}
	return string(b)
}

// GroupCount x
func GroupCount(input string) int {
	count, _, _ := Process(input)
	return count
}

// GroupScore x
func GroupScore(input string) int {
	_, score, _ := Process(input)
	return score
}

func GarbageCount(input string) int {
	_, _, gc := Process(input)
	return gc
}

func main() {
	// fmt.Println("Hello, world")
	// fmt.Println(Process("{{{}}}"))
	// fmt.Println(Process("{{},{}}"))
	text := ReadFile("../input.txt")
	count, score, gcount := Process(text)
	fmt.Println("Part1:")
	fmt.Printf("Count[%v] Score[%v]\n", count, score)
	fmt.Println("Part2:")
	fmt.Printf("GCount[%v]\n", gcount)
}
