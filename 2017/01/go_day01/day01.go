// Package main provides ...
package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func Part1(numsStr string) int {
	return Captcha(numsStr, 1)
}

func Part2(numsStr string) int {
	rotateAmount := len(numsStr) / 2
	return Captcha(numsStr, rotateAmount)
}

func Captcha(numsStr string, rotateAmount int) int {
	s1 := []rune(numsStr)
	s2 := []rune(Rotate(numsStr, rotateAmount))
	count := 0
	for i := range s1 {
		c1 := s1[i]
		c2 := s2[i]
		if c1 == c2 {
			// Convert rune to int. Example: char '9' to int 9
			val := int(c1 - '0')
			count += val
		}
	}
	return count
}

func Rotate(input string, rotateAmount int) string {
	offset := rotateAmount % len(input)
	begin := offset
	end := offset + len(input)
	output := strings.Repeat(input, 2)
	return output[begin:end]
}

func main() {
	input, err := ioutil.ReadFile("../input.txt")
	if err != nil {
		fmt.Print(err)
	}
	inputStr := strings.TrimSpace(string(input))
	fmt.Println("Part1:")
	fmt.Println(Part1(inputStr))
	fmt.Println("Part2:")
	fmt.Println(Part2(inputStr))
}
