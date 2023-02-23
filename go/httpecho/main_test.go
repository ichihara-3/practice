package main

import (
	"bytes"
	"net/http"
	"testing"
)

func TestEcho(t *testing.T) {
	want := []byte("Hello, World")
	in, _ := http.NewRequest("GET", "http://test.test", bytes.NewBuffer(want))
	got := Echo(in)
	if bytes.Compare(want, got) != 0 {
		t.Errorf("want: %v, got: %v\n", want, got)
	}
}
