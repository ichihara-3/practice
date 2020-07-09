package main

import (
	"fmt"
	"path/filepath"
)

func main() {
	fmt.Println(filepath.Clean("."))
	fmt.Println(filepath.Clean(".//hello"))
	fmt.Println(filepath.Clean("./hello"))
	fmt.Println(filepath.Clean("~"))
	fmt.Println(filepath.Clean("//hello\\/.world/"))
}
