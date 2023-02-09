// Package main provides ...
package main

import "fmt"
import "os"
import "bufio"
import "log"
import "strconv"
import "container/heap"

// An IntHeap is a max-heap of ints.
type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *IntHeap) Push(x any) {
	// Push and Pop use pointer receivers because they modify the slice's length,
	// not just its contents.
	*h = append(*h, x.(int))
}

func (h *IntHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func Parse(filename string) [][]int {
	outer := make([][]int, 0)
	inner := make([]int, 0)

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {

		text := scanner.Text()
		if text == "" {
			outer = append(outer, inner)
			inner = make([]int, 0)
			continue
		}

		num, err := strconv.Atoi(text)
		if err != nil {
			log.Fatal(err)
		}
		inner = append(inner, num)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	outer = append(outer, inner)
	return outer
}

func elfCalories(elf []int) int {
	calories := 0
	for _, item := range elf {
		calories += item
	}
	return calories
}

func PartOne(elves [][]int) int {
	maxCalories := 0

	for _, elf := range elves {
		calories := elfCalories(elf)
		if calories > maxCalories {
			maxCalories = calories
		}
	}
	return maxCalories
}

func PartTwo(elves [][]int) int {
	h := &IntHeap{}
	heap.Init(h)

	for _, elf := range elves {
		calories := elfCalories(elf)
		heap.Push(h, calories)
	}

	topThree := 0
	for i := 0; i < 3; i++ {
		topThree += heap.Pop(h).(int)
	}
	return topThree
}

func main() {
	elves := Parse("../../inputs/01/input.txt")

	fmt.Print("Part 1: ")
	fmt.Println(PartOne(elves))
	fmt.Print("Part 2: ")
	fmt.Println(PartTwo(elves))
}
