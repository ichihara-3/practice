package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

func main() {
	flag.Parse()
	if flag.NArg() != 1 {
		log.Fatal("a filename is expected")
	}
	fileName := flag.Arg(0)
	f, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	buf := make([]byte, 1024)
	f.Read(buf)
	fmt.Println(string(buf))
}
