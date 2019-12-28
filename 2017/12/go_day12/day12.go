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

type Rule struct {
	Left  int
	Right []int
}

type Groupings struct {
	WhichSet map[int]int
	Sets     []map[int]bool
}

// Parse turns a filename into a slice of Rule.
// A single line might look like:
// 4 <-> 2, 3, 6
// That rule would be Rule{Left: 4, Right: []int{2, 3, 6}}
// Parse returns a slice of these rules.
func Parse(filename string) []Rule {
	rules := make([]Rule, 0)

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		leftRight := strings.Split(line, " <-> ")

		left, err := strconv.Atoi(leftRight[0])
		if err != nil {
			log.Fatal(err)
		}

		rightStrs := strings.Split(leftRight[1], ", ")
		rights := make([]int, 0)
		for _, item := range rightStrs {
			right_num, err := strconv.Atoi(item)
			if err != nil {
				log.Fatal(err)
			}
			rights = append(rights, right_num)
		}

		rule := Rule{Left: left, Right: rights}
		rules = append(rules, rule)
	}

	return rules
}

func BuildGroupings(rules []Rule) Groupings {
	g := Groupings{WhichSet: make(map[int]int, 0)}
	for _, rule := range rules {
		list := append(rule.Right, rule.Left)
		g.AddLinkedNumbers(list)
	}
	return g
}

func (g *Groupings) MergeSets(i int, j int) {
	// For each item in the J set, add it to the I set
	for num, _ := range g.Sets[j] {
		g.Sets[i][num] = true
	}

	// Set the J set to nothing
	g.Sets[j] = make(map[int]bool, 0)

	// Anything that has "J" in the lookup table is moved to "I"
	for num, setIndex := range g.WhichSet {
		if setIndex == j {
			g.WhichSet[num] = i
		}
	}
}

func (g *Groupings) AddLinkedNumbers(nums []int) {
	// Does any number exist?
	setsSeen := make(map[int]bool, 0)
	for _, num := range nums {
		if i, ok := g.WhichSet[num]; ok {
			setsSeen[i] = true
		}
	}

	// If we saw multiple sets, merge them into the first set
	firstI := -1
	for i := range setsSeen {
		if firstI == -1 {
			firstI = i
		} else {
			g.MergeSets(firstI, i)
		}
	}

	if len(setsSeen) == 0 {
		// Create a new set of linked numbers
		newSet := make(map[int]bool, 0)
		for _, num := range nums {
			newSet[num] = true
		}
		// Add the set to g.Sets
		g.Sets = append(g.Sets, newSet)

		// Mark each number as belonging in the new set
		newSetIndex := len(g.Sets) - 1
		for _, num := range nums {
			g.WhichSet[num] = newSetIndex
		}
	} else {
		// At least one of the numbers exists in set i
		// Add the rest
		for _, num := range nums {
			// Check if it's not added already
			if _, ok := g.WhichSet[num]; !ok {
				g.WhichSet[num] = firstI
				g.Sets[firstI][num] = true
			}
		}
	}
}

// Part1 answers How many programs are in the group that contains program ID
func Part1(g Groupings) int {
	setIndex := g.WhichSet[0]
	count := 0
	for _, v := range g.Sets[setIndex] {
		if v {
			count += 1
		}
	}
	return count
}

// Part2 answers How many groups are there in total?
// We have to be careful, since some sets might be empty after merging
func Part2(g Groupings) int {
	count := 0
	for _, set := range g.Sets {
		if len(set) > 0 {
			count += 1
		}
	}
	return count
}

func main() {
	rules := Parse("../input.txt")
	groupings := BuildGroupings(rules)

	p1Ans := Part1(groupings)
	fmt.Println("Part 1:")
	fmt.Println(p1Ans)

	p2Ans := Part2(groupings)
	fmt.Println("Part 2:")
	fmt.Println(p2Ans)
}
