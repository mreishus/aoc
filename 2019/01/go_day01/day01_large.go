// Package main provides ...
package main

import (
	"bufio"
	"fmt"
	"log"
	"math/big"
	"os"
	"strings"
)

var zero = big.NewInt(0)
var two = big.NewInt(2)
var three = big.NewInt(3)

func Fuel(x *big.Int) *big.Int {
	x = x.Div(x, three)
	return x.Sub(x, two)
}

func TotalFuel(fuel big.Int) big.Int {
	total := big.NewInt(0)
	for {
		fuel = *Fuel(&fuel)
		if fuel.Cmp(zero) == -1 {
			break
		}
		total.Add(total, &fuel)
	}
	return *total
}

func Parse(filename string) []*big.Int {
	lines := make([]*big.Int, 0)
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		num := new(big.Int)
		num, ok := num.SetString(strings.TrimSpace(line), 10)
		if !ok {
			log.Fatal("SetString failed")
		}
		lines = append(lines, num)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return lines
}

func Part1(nums []*big.Int) *big.Int {
	total := big.NewInt(0)
	for _, num := range nums {
		total.Add(total, Fuel(num))
	}
	return total
}

func Part2(nums []*big.Int) *big.Int {
	messages := make(chan big.Int)
	total := big.NewInt(0)
	for _, num := range nums {
		n := *num
		go func() {
			messages <- TotalFuel(n)
		}()
	}
	for range nums {
		x := <-messages
		total.Add(total, &x)
	}
	return total
}

func main() {
	// nums := Parse("../input_large.txt")
	nums := Parse("../input_large.txt")
	fmt.Println("AOC 2019 Day 01: (Large Input)")
	fmt.Println("Part1:")
	fmt.Println(Part1(nums))
	nums = Parse("../input_large.txt")
	fmt.Println("Part2 (Large Input):")
	fmt.Println(Part2(nums))
}
