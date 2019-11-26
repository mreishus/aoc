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

func AddOne(x int) int {
	return x + 1
}

// Parse (Filename) -> Spreadsheet
func Parse(filename string) [][]int {
	spreadSheet := make([][]int, 0)

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		numsThisLine, err := sliceAtoi(strings.Fields(scanner.Text()))
		if err != nil {
			return spreadSheet
		}
		spreadSheet = append(spreadSheet, numsThisLine)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return spreadSheet
}

// sliceAtoi (Slice of strings) -> Slice of Ints
func sliceAtoi(strings []string) ([]int, error) {
	ints := make([]int, 0)
	for _, str := range strings {
		num, err := strconv.Atoi(str)
		if err != nil {
			return ints, err
		}
		ints = append(ints, num)
	}

	return ints, nil
}

// Part1 : Sum up all the checksums of a spreadsheet
func Part1(spreadSheet [][]int) int {
	checksums := 0
	for _, row := range spreadSheet {
		checksum := Checksum(row)
		checksums += checksum
	}
	return checksums
}

func Checksum(row []int) int {
	min, max := MinMax(row)
	return max - min
}

func MinMax(row []int) (int, int) {
	var min int = row[0]
	var max int = row[0]
	for _, value := range row {
		if value < min {
			min = value
		}
		if value > max {
			max = value
		}
	}
	return min, max
}

func main() {
	spreadSheet := Parse("../input.txt")
	checkSum := Part1(spreadSheet)
	fmt.Println("Part1")
	fmt.Println(checkSum)
}
