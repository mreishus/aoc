package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Coord struct {
	X, Y int
}
type Wire struct {
	Steps []WireStep
}
type WireStep struct {
	Direction string
	Distance  int
}

func (w *Wire) AddStep(ws WireStep) {
	w.Steps = append(w.Steps, ws)
}

func Parse(filename string) []Wire {
	wires := make([]Wire, 0)
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		wire := ParseLine(line)
		wires = append(wires, wire)
	}

	return wires
}

func ParseLine(line string) Wire {
	wire := Wire{}

	for _, stepStr := range strings.Split(line, ",") {
		wire.AddStep(ParseStep(stepStr))
	}

	return wire
}

// ParseStep parses a single step string, like "U10".
func ParseStep(stepStr string) WireStep {
	direction := stepStr[0:1]
	distance, err := strconv.Atoi(stepStr[1:])
	if err != nil {
		log.Fatal("Couldn't parse distance")
	}
	return WireStep{Direction: direction, Distance: distance}
}

// Move moves a coordinate by one step in the specified direction.
func Move(where Coord, direction string) Coord {
	switch direction {
	case "R":
		return Coord{where.X + 1, where.Y}
	case "L":
		return Coord{where.X - 1, where.Y}
	case "U":
		return Coord{where.X, where.Y + 1}
	case "D":
		return Coord{where.X, where.Y - 1}
	}
	log.Fatal("Unknown direction")
	return where
}

func Manhattan(where Coord) int {
	return Abs(where.X) + Abs(where.Y)
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// Solve possibly needs a refactor.
func Solve(wires []Wire) (int, int) {
	// Trace wires and Build Grid
	gridWireIDs := make(map[Coord][]int)
	gridSteps := make(map[Coord][]int)

	for wireID, wire := range wires {
		location := Coord{0, 0}
		steps := 0
		for _, step := range wire.Steps {
			for i := 0; i < step.Distance; i++ {
				location = Move(location, step.Direction)
				steps++

				if !contains(gridWireIDs[location], wireID) {
					gridWireIDs[location] = append(gridWireIDs[location], wireID)
					gridSteps[location] = append(gridSteps[location], steps)
				}
			}
		}
	}

	// Build Intersections
	intersections := make([]Coord, 0)
	for coord, v := range gridWireIDs {
		if len(v) > 1 {
			intersections = append(intersections, coord)
		}
	}

	// Find Minimums needed for part1 and part2 of problem
	smallestManhattan := 9999999
	smallestStepSum := 9999999

	for _, coord := range intersections {
		// Part1: Smallest manhattan
		mDist := Manhattan(coord)
		if mDist < smallestManhattan {
			smallestManhattan = mDist
		}

		// Part2: Smallest Step Sum
		stepSum := sum(gridSteps[coord])
		if stepSum < smallestStepSum {
			smallestStepSum = stepSum
		}
	}

	return smallestManhattan, smallestStepSum
}

func sum(nums []int) int {
	answer := 0
	for _, item := range nums {
		answer += item
	}
	return answer
}

func contains(haystack []int, target int) bool {
	for _, item := range haystack {
		if item == target {
			return true
		}
	}
	return false
}

func main() {
	// wires := Parse("../input_small.txt")
	wires := Parse("../input.txt")
	answer1, answer2 := Solve(wires)
	fmt.Println("AOC 2019 Day 03:")
	fmt.Println("Part 1:")
	fmt.Println(answer1)
	fmt.Println("Part 2:")
	fmt.Println(answer2)
}
