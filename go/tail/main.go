package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"os"
)

var DEFAULT_N_LINE int = 10

var BUFSIZE int64 = 10 * 1024 * 1024

func main() {
	var nFlag = flag.Int("n", DEFAULT_N_LINE, "number of lines to show")
	flag.Parse()
	if flag.NArg() != 1 {
		log.Fatal("a filename is expected")
	}
	fileName := flag.Arg(0)
	f, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}

	fs, err := f.Stat()
	if err != nil {
		log.Fatal(err)
	}

	var n_line = *nFlag
	lines := make([][]byte, 0, n_line)

	offset := fs.Size() - 1
	var end int64

	var restbuf = make([]byte, 0, BUFSIZE)

	for offset > 0 {
		if offset >= BUFSIZE {
			end = BUFSIZE
			offset -= BUFSIZE
		} else {
			end = offset
			offset = 0
		}
		buf := make([]byte, end)
		n, err := f.ReadAt(buf, offset)
		if err != nil {
			if err != io.EOF {
				log.Fatal(err)
			}
		}

		for n--; n >= 0; n-- {
			if buf[n] == 0x0a {
				lines = append(lines, Concatenate(buf[n+1:end], restbuf))
				restbuf = make([]byte, 0, BUFSIZE)
				end = int64(n)
				if len(lines) == n_line {
					break
				}
			}
		}
		if len(lines) < n_line {
			restbuf = Concatenate(buf[0:end], restbuf)
		} else {
			break
		}
	}
	if len(lines) != n_line && end > 0 {
		lines = append(lines, restbuf)
	}

	for i := len(lines) - 1; i >= 0; i-- {
		fmt.Println(string(lines[i]))
	}
}

func Concatenate(one []byte, another []byte) []byte {
	tmp := make([]byte, len(one), len(one)+len(another))
	copy(tmp, one)
	return append(tmp, another...)
}
