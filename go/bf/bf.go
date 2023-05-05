package main

import (
	"fmt"
	"io"
	"log"
	"os"
)

func main() {
	buf := make([]int, 30000)
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "no program given as an argument")
		os.Exit(1)
	}
	program := os.Args[1]
	Bf(program, buf, os.Stdin, os.Stdout)
}

func Bf(program string, buf []int, r io.Reader, w io.Writer) {
	var (
		ptr     = 0
		codeptr = 0
		stack   = make([]int, 0)
	)

	for codeptr < len(program) {
		c := program[codeptr]
		if c == '>' {
			ptr++
		} else if c == '<' {
			ptr--
		} else if c == '+' {
			buf[ptr]++
		} else if c == '-' {
			buf[ptr]--
		} else if c == '.' {
			bs := []byte(string(rune(buf[ptr])))
			w.Write(bs)
		} else if c == ',' {
			b := make([]byte, 1)
			_, err := r.Read(b)
			if err != nil {
				log.Fatal(err)
			}
			buf[ptr] = int(b[0])
		} else if c == '[' {
			if buf[ptr] == 0 {
				for codeptr < len(program) {
					if program[codeptr] == ']' {
						codeptr++
						break
					}
				}
			}	else {
				stack = append(stack, codeptr)
			}
		} else if c == ']' {
			if buf[ptr] != 0 {
				codeptr = stack[len(stack)-1]
			} else {
				stack = stack[:len(stack)-1]
			}
		}
		codeptr++
	}
}
