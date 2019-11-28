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

// ParsedNode x
type ParsedNode struct {
	Name   string
	Weight int
	Right  []string
}

// Node X
type Node struct {
	Name     string
	Weight   int
	Children []*Node
	Parent   *Node
}

// Tree X
type Tree struct {
	Root *Node
}

// Parse x
func Parse(filename string) []ParsedNode {
	nodes := make([]ParsedNode, 0)

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

// ParseLine X
func ParseLine(line string) ParsedNode {
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
	return ParsedNode{Name: name, Weight: weight, Right: above}
}

func makeDirectionMaps(nodes []ParsedNode) (leftOf map[string]string, rightOf map[string][]string) {
	leftOf = make(map[string]string, 0)
	rightOf = make(map[string][]string, 0)

	// fmt.Println("part1")
	// fmt.Printf("%v\n", nodes)
	for _, node := range nodes {
		for _, rightStr := range node.Right {
			if rightStr == "" {
				continue
			}
			// We know that name `node.Name` has name `rightStr` above it.
			leftOf[rightStr] = node.Name
			rightOf[node.Name] = append(rightOf[node.Name], rightStr)
		}
	}
	return leftOf, rightOf
}

func makeNameLookup(nodes []ParsedNode) map[string]ParsedNode {
	nodesByName := make(map[string]ParsedNode, 0)
	for _, node := range nodes {
		nodesByName[node.Name] = node
	}
	return nodesByName
}

// GetLeftNode X
func GetLeftNode(nodes []ParsedNode) ParsedNode {
	leftOf, _ := makeDirectionMaps(nodes)
	nodesByName := makeNameLookup(nodes)

	// What is the left most?
	// Pick any node, then look left
	node := nodes[0]
	for {
		parent := leftOf[node.Name]
		if parent == "" {
			break
		}
		node = nodesByName[parent]
	}

	// Build Tree
	return node
}

func MakeTree(nodes []ParsedNode) Tree {
	_, rightOf := makeDirectionMaps(nodes)
	nodesByName := makeNameLookup(nodes)
	leftNode := GetLeftNode(nodes)

	root := buildNode(leftNode.Name, nodesByName, rightOf)
	return Tree{Root: root}
}

func buildNode(name string, nodesByName map[string]ParsedNode, rightOf map[string][]string) *Node {
	temp := nodesByName[name]
	node := Node{
		Name:   name,
		Weight: temp.Weight,
	}
	for _, rightName := range rightOf[name] {
		node.Children = append(node.Children, buildNode(rightName, nodesByName, rightOf))
	}
	return &node
}

func weightSum(node *Node) int {
	w := node.Weight
	for _, c := range node.Children {
		w += weightSum(c)
	}
	return w
}

// Part1 x
func Part1(nodes []ParsedNode) {
	node := GetLeftNode(nodes)
	fmt.Printf("The bottom node is: %v\n", node)
}

// Part2 x
func Part2(nodes []ParsedNode) {
	t := MakeTree(nodes)
	a := findImbalance(t.Root, 0)
	fmt.Println(a)
}

func findImbalance(node *Node, delta int) int {
	// Calculate normal weight
	childWeights := make([]int, 0)
	for _, child := range node.Children {
		w := weightSum(child)
		childWeights = append(childWeights, w)
	}
	normalWeight := getMode(childWeights)

	// seenDifferentWeight := false
	for _, child := range node.Children {
		w := weightSum(child)
		if w != normalWeight {
			// seenDifferentWeight := true
			delta := normalWeight - w
			return findImbalance(child, delta)
		}
	}

	return node.Weight + delta
}

func getMode(inputArray []int) (mode int) {
	//	Create a map and populated it with each value in the slice
	//	mapped to the number of times it occurs
	countMap := make(map[int]int)
	for _, value := range inputArray {
		countMap[value]++
	}

	//	Find the smallest item with greatest number of occurance in
	//	the input slice
	max := 0
	for _, key := range inputArray {
		freq := countMap[key]
		if freq > max {
			mode = key
			max = freq
		}
	}
	return mode
}

func main() {
	nodes := Parse("../input_small.txt")
	fmt.Println("InputSmall")
	fmt.Println("Part1")
	Part1(nodes)
	fmt.Println("Part2")
	Part2(nodes)

	nodes = Parse("../input.txt")
	fmt.Println("\nInput")
	fmt.Println("Part1")
	Part1(nodes)
	fmt.Println("Part2")
	Part2(nodes)
}
