package main

import (
	"fmt"
	"strings"
)

func gogo(n int, c chan int) {
	fmt.Println(strings.Repeat("gogo", n))
	c <- 0
}

func main() {
	var n int
	fmt.Scan(&n)
	c := make(chan int)
	go gogo(n, c)
	res := <-c

	if res != 0 {
		panic("error")
	}
}
