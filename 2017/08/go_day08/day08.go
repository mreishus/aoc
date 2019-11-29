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

type Instruction struct {
	Register          string
	Increment         bool
	Amount            int
	ConditionRegister string
	Operand           string
	ConditionValue    int
}

// AddOne x
func AddOne(x int) int {
	return x + 1
}

// ParseLine x
func ParseLine(line string) Instruction {
	fields := strings.Fields(line)

	amount, err1 := strconv.Atoi(fields[2])
	value, err2 := strconv.Atoi(fields[6])
	i := Instruction{
		Register:          fields[0],
		Increment:         fields[1] == "inc",
		Amount:            amount,
		ConditionRegister: fields[4],
		Operand:           fields[5],
		ConditionValue:    value,
	}
	if err1 != nil || err2 != nil {
		log.Fatal("Couldnt parse amount")
	}
	// fmt.Printf("Reg[%v] Inc[%v] Amount[%v] CReg[%v] Operand[%v] value[%v]\n", i.Register, i.Increment, i.Amount, i.ConditionRegister, i.Operand, i.ConditionValue)

	return i
}

// Parse x
func Parse(filename string) []Instruction {
	instructions := make([]Instruction, 0)
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println("--")
		// fmt.Println(line)

		instruction := ParseLine(line)
		instructions = append(instructions, instruction)
		// fmt.Printf("%v\n", n)
		// fmt.Println("")
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return instructions
}

// Part1 x
func Part1(filename string) {
	fmt.Printf("Part1 file[%v]\n", filename)
	instructions := Parse(filename)
	registers := make(map[string]int, 0)
	registers = RunInstructions(instructions, registers)
	max := maxRegValue(registers)
	fmt.Printf("Max value: [%v]\n", max)
}

func maxRegValue(registers map[string]int) int {
	max := -99999
	for _, value := range registers {
		if value > max {
			max = value
		}
	}
	return max
}

// RunInstructions x
func RunInstructions(program []Instruction, registers map[string]int) map[string]int {
	for _, instr := range program {
		v1 := registers[instr.ConditionRegister]
		v2 := instr.ConditionValue
		var result bool
		switch instr.Operand {
		case ">":
			result = v1 > v2
		case ">=":
			result = v1 >= v2
		case "<":
			result = v1 < v2
		case "<=":
			result = v1 <= v2
		case "==":
			result = v1 == v2
		case "!=":
			result = v1 != v2
		}
		if result {
			// fmt.Printf("++ True\n")
			if instr.Increment {
				registers[instr.Register] += instr.Amount
				// fmt.Printf("    Adding %v to %v --> [%v]\n", instr.Amount, instr.Register, registers[instr.Register])
			} else {
				registers[instr.Register] -= instr.Amount
				// fmt.Printf("    Subtracting %v from %v --> [%v]\n", instr.Amount, instr.Register, registers[instr.Register])
			}
		} else {
			// fmt.Printf("-- False\n")
		}
	}
	return registers
}

func main() {
	Part1("../input_small.txt")
	Part1("../input.txt")
}
