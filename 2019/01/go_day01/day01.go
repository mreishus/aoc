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

func Fuel(x int) int {
	return x/3 - 2
}

func TotalFuel(fuel int) int {
	total := 0
	for {
		fuel = Fuel(fuel)
		if fuel <= 0 {
			break
		}
		total += fuel
	}
	return total
}

func Parse(filename string) []int {
	lines := make([]int, 0)
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		num, err := strconv.Atoi(strings.TrimSpace(line))
		if err != nil {
			log.Fatal(err)
		}
		lines = append(lines, num)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return lines
}

func Part1(nums []int) int {
	total := 0
	for _, num := range nums {
		total += Fuel(num)
	}
	return total
}
func Part2(nums []int) int {
	total := 0
	for _, num := range nums {
		total += TotalFuel(num)
	}
	return total
}

func main() {
	nums := Parse("../input.txt")
	fmt.Println("AOC 2019 Day 01:")
	fmt.Println("Part1:")
	fmt.Println(Part1(nums))
	fmt.Println("Part2:")
	fmt.Println(Part2(nums))
}
