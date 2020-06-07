package main

import (
	"bytes"
	"encoding/binary"
	"flag"
	"os"
)

func main() {
	buf := new(bytes.Buffer)
	var i = flag.Uint("i", 0, "an integer to write")
	var num uint
	flag.Parse()
	num = *i
	err := binary.Write(buf, binary.LittleEndian, uint8(num))
	if err != nil {
		panic("failed to write a number")
	}
	os.Stdout.Write(buf.Bytes())
}
