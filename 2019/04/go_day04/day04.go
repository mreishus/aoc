// Package main provides ...
package main

import (
	"fmt"
	"log"
	"strconv"
)

func Solve(low, high int) int {
	count := 0
	for i := low; i < high; i++ {
		if IsPassword(i) {
			count += 1
		}
	}
	return count
}
func Solve2(low, high int) int {
	count := 0
	for i := low; i < high; i++ {
		if IsPassword2(i) {
			count += 1
		}
	}
	return count
}

func IsPassword(x int) bool {
	return IsSixDigits(x) && IsMonoInc(x) && IsPart1(x)
}

func IsPassword2(x int) bool {
	return IsSixDigits(x) && IsMonoInc(x) && IsPart2(x)
}

func IsSixDigits(x int) bool {
	return x >= 100000 && x <= 999999
}

// IsMonoInc Are the digits of a number monotonically increasing?
func IsMonoInc(x int) bool {
	xStr := strconv.Itoa(x)
	lastDigit := 0
	for _, char := range xStr {
		digit, err := strconv.Atoi(string(char))
		if err != nil {
			log.Fatal("Couldn't parse")
		}
		if digit < lastDigit {
			return false
		}
		lastDigit = digit
	}
	return true
}

func IsPart1(x int) bool {
	freq := DigitFrequency(x)
	for _, v := range freq {
		if v >= 2 {
			return true
		}
	}
	return false
}

func IsPart2(x int) bool {
	freq := DigitFrequency(x)
	for _, v := range freq {
		if v == 2 {
			return true
		}
	}
	return false
}

func DigitFrequency(x int) map[int]int {
	freq := make(map[int]int, 0)
	xStr := strconv.Itoa(x)
	for _, char := range xStr {
		digit, err := strconv.Atoi(string(char))
		if err != nil {
			log.Fatal("Couldn't parse")
		}
		freq[digit]++
	}
	return freq
}

func main() {
	fmt.Println("AOC 2019 Day 4")
	fmt.Println("Part1: ")
	fmt.Println(Solve(245182, 790572))
	fmt.Println("Part2: ")
	fmt.Println(Solve2(245182, 790572))
}
