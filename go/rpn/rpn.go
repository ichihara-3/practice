package rpn

import (
	"log"
	"strconv"
	"strings"
)

func rpn(line string) int {
	// split line into tokens by spaces
	tokens := strings.Split(line, " ")
	// create a stack
	stack := new(Stack)
	// for each token in tokens
	for _, token := range tokens {
		if isOperator(token) {
			v1 := stack.Pop()
			v2 := stack.Pop()
			switch token {
			case "+":
				stack.Push(v2 + v1)
			case "-":
				stack.Push(v2 - v1)
			case "*":
				stack.Push(v2 * v1)
			case "/":
				stack.Push(v2 / v1)
			}
		} else {
			v, err := strconv.Atoi(token)
			if err != nil {
				log.Fatal(err)
			}
			stack.Push(v)
		}
	}
	// length of stack should be 1
	if stack.Len() != 1 {
		log.Fatal("Invalid RPN expression")
	}
	return stack.Pop()
}

func isOperator(token string) bool {
	return token == "+" || token == "-" || token == "*" || token == "/"
}

type Stack struct {
	top  *Element
	size int
}

type Element struct {
	value int
	next  *Element
}

func (s *Stack) Len() int {
	return s.size
}

func (s *Stack) Push(value int) {
	s.top = &Element{value, s.top}
	s.size++
}
func (s *Stack) Pop() (value int) {
	if s.size > 0 {
		value, s.top = s.top.value, s.top.next
		s.size--
		return
	}
	return 0
}
