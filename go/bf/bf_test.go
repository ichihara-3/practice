// test for Go-Brainfuck implementation

package main

import (
	"bytes"
	"io"
	"testing"
)

func TestBfPlus(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := "++"
	want := 2
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	if buf[0] != want {
		t.Errorf("Brainfuck() results %v, want: %v", buf[0], want)
	}
}

func TestBfMinus(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := "--"
	want := -2
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	if buf[0] != want {
		t.Errorf("Brainfuck() results %v, want: %v", buf[0], want)
	}
}

func TestBfIncPtr(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := ">++"
	want := 2
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	if buf[1] != want {
		t.Errorf("Brainfuck() results %v, want: %v", buf[0], want)
	}
}

func TestBfDecPtr(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := ">>><<++"
	want := 2
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	if buf[1] != want {
		t.Errorf("Brainfuck() results %v, want: %v", buf[0], want)
	}
}

func TestBfInput(t *testing.T) {
	r := bytes.NewBufferString("1")
	w := new(bytes.Buffer)
	given := ","
	want := 49 // "1" literal is 49th unicode char
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	if buf[0] != want {
		t.Errorf("Brainfuck() results %v, want: %v", buf[0], want)
	}
}

func TestBfPrint(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := "+++++++++++++++++++++++++++++++++++++++++++++++++."
	want := "1"
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	res := make([]byte, 1000)
	n, err := w.Read(res)
	if err != nil {
		if err != io.EOF{
			t.Fatal(err)
		}
	}
	if string(res[:n]) != want {
		t.Errorf("Brainfuck() results %v, want: %v", string(res[:n]), want)
	}
}

func TestBfLoop(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := "+++[>+++<-]"
	want := 9
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	if buf[1] != want {
		t.Errorf("Brainfuck() results %v, want: %v", buf[0], want)
	}
}

// given bf program that indicates to print "Hello, World!"
func TestBfHelloWorld(t *testing.T) {
	r := bytes.NewBufferString("")
	w := new(bytes.Buffer)
	given := "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
	buf := make([]int, 30000)
	Bf(given, buf, r, w)
	res := make([]byte, 1000)
	n, err := w.Read(res)
	if err != nil {
		if err != io.EOF {
			t.Fatal(err)
		}
	}
	want := "Hello World!\n"
	if string(res[:n]) != want {
		t.Errorf("Brainfuck() results %v, want: %v", string(res[:n]), want)
	}
}
