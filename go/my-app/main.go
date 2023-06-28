package main

import "fmt"

func main() {
	fmt.Println("こんにちは、世界")
	const (
		Apple = iota
		Orange
		Banana
	)
	fmt.Println(Apple)
	fmt.Println(Orange)
	fmt.Println(Banana)
	a := Apple
	switch a {
	case 0:
		fmt.Println("Apple")
	case 1:
		fmt.Println("Orange")
	case 2:
		fmt.Println("Banana")
	default:
		fmt.Println("Not found")
	}
}
