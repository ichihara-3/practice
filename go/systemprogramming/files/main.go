// open files and output to stdout

package main

import (
	"io"
	"log"
	"os"
	"time"
	"fmt"
)

func main() {
	file, err := os.Create("log.txt")
	if err != nil {
		log.Fatal(err)
	}
	writer := io.MultiWriter(os.Stdout, file)
	io.Copy(writer, MyLogger(os.Stdin))
}

type myLogger struct {
	r io.Reader
}

func MyLogger(r io.Reader) *myLogger {
	return &myLogger{r: r}
}

func (l *myLogger) Read(p []byte) (n int, err error) {
	now := fmt.Sprintf("[%s] ", time.Now().Format(time.RFC3339))
	copy(p, now)
	n, err = l.r.Read(p[len(now):])
	if err != nil {
		return n, err
	}
	return n + len(now), nil
}