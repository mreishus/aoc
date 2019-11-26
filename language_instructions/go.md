 # Go
 
 ## Basic Setup
 
 ```fish
 set PROJNAME go_day01
 mkdir $PROJNAME
 cd $PROJNAME
 nvim day01.go day01_test.go Makefile -p
 ```
 
 ## `day01.go`
 
 ```
// Package main provides ...
package main

import "fmt"

func AddOne(x int) int {
	return x + 1
}

func main() {
	fmt.Println("Hello, world")
}
 ```
 
 ## `day01_test.go`
 
 ```
// Package main provides ...
package main

import "testing"

func TestAddOne(t *testing.T) {
	t.Run("It adds one", func(t *testing.T) {
		got := AddOne(1)
		want := 2
		if got != want {
			t.Errorf("got %q want %q", got, want)
		}
	})
}

 ```
 
 ## `Makefile`
 
 ```
 run:
	go run day01.go
test:
	go test
format:
	go fmt
repl:
	echo Visit https://play.golang.org/ I guess?
 ```
