// Package main provides ...
package main

import (
	"fmt"
	"io/ioutil"
)

// Process x
func Process(input string) (int, int) {
	groupsDeep := 0
	groupCount := 0
	ignoreNext := false
	inGarbage := false
	score := 0

	for _, s := range input {
		if ignoreNext {
			ignoreNext = false
			continue
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
	return groupCount, score
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
	count, _ := Process(input)
	return count
}

// GroupScore x
func GroupScore(input string) int {
	_, score := Process(input)
	return score
}

func main() {
	// fmt.Println("Hello, world")
	// fmt.Println(Process("{{{}}}"))
	// fmt.Println(Process("{{},{}}"))
	text := ReadFile("../input.txt")
	count, score := Process(text)
	fmt.Println("Part1:")
	fmt.Printf("Count[%v] Score[%v]\n", count, score)
}
