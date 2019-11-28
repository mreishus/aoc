// Package main provides ...
package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// Node x
type Node struct {
	Name   string
	Weight int
	Above  []string
}

// AddOne x
func AddOne(x int) int {
	return x + 1
}

// Parse x
func Parse(filename string) []Node {
	nodes := make([]Node, 0)

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println(line)
		n := ParseLine(line)
		nodes = append(nodes, n)
		// fmt.Printf("%v\n", n)
		// fmt.Println("")
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return nodes
}

func ParseLine(line string) Node {
	// ymyzead (76)
	// srcyajr (77) -> vxjjxhz, aevhbim, sldytqh
	re := regexp.MustCompile(`^(\w+) \((\d+)\)( -> (.*))?$`)
	matches := re.FindStringSubmatch(line)
	// fmt.Printf("%q\n", matches)

	name := matches[1]
	weight, _ := strconv.Atoi(matches[2])
	aboveStr := matches[4]
	above := strings.Split(aboveStr, ", ")

	// fmt.Printf("name[%v] weight[%v] aboveStr[%v] above[%q]\n", name, weight, aboveStr, above)
	return Node{Name: name, Weight: weight, Above: above}
}

func GetBottomNode(nodes []Node) Node {
	below := make(map[string]string, 0)
	nodesByName := make(map[string]Node, 0)

	// fmt.Println("part1")
	// fmt.Printf("%v\n", nodes)
	for _, node := range nodes {
		nodesByName[node.Name] = node
		for _, above := range node.Above {
			if above == "" {
				continue
			}
			// We know that name `node.Name` has name `above` above it.
			below[above] = node.Name
		}
	}

	// What is the bottom?
	// Pick any node, then look up the tree
	node := nodes[0]
	for {
		belowMe := below[node.Name]
		if belowMe == "" {
			break
		}
		node = nodesByName[belowMe]
	}
	return node
}

// Part1 x
func Part1(nodes []Node) {
	node := GetBottomNode(nodes)
	fmt.Printf("The bottom node is: %v\n", node)
}

func main() {
	fmt.Println("Hello, world")
	nodes := Parse("../input_small.txt")
	Part1(nodes)
	nodes = Parse("../input.txt")
	Part1(nodes)
}
