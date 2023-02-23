package main

import (
	"io"
	"log"
	"net/http"
)

func Echo(input *http.Request) []byte {
	buf := make([]byte, 4096)
	n, err := input.Body.Read(buf)
	if err != nil {
		if err != io.EOF {
			log.Fatal(err)
		}
	}
	return buf[0:n]
}

func handleEcho(w http.ResponseWriter, r *http.Request) {
	w.Write(Echo(r))
}

func main() {
	http.HandleFunc("/echo", handleEcho)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
