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
	count := flag.NArg()
	if count < 1 {
		log.Fatal("a filename is expected")
	}
	fileNames := flag.Args()
	for i, name := range fileNames {
		f, err := os.Open(name)
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
					lines = append(lines, concatenate(buf[n+1:end], restbuf))
					restbuf = make([]byte, 0, BUFSIZE)
					end = int64(n)
					if len(lines) == n_line {
						break
					}
				}
			}
			if len(lines) < n_line {
				restbuf = concatenate(buf[0:end], restbuf)
			} else {
				break
			}
		}
		if len(lines) != n_line && end > 0 {
			lines = append(lines, restbuf)
		}

		if count >= 2 {
			printFilename(name)
		}

		for i := len(lines) - 1; i >= 0; i-- {
			fmt.Println(string(lines[i]))
		}

		if i < count-1 {
			printBalnkline()
		}
	}
}

func concatenate(one []byte, another []byte) []byte {
	tmp := make([]byte, len(one), len(one)+len(another))
	copy(tmp, one)
	return append(tmp, another...)
}

func printFilename(name string) {
	fmt.Printf("==> %s <==\n", name)
}

func printBalnkline() {
	fmt.Printf("\n")
}
