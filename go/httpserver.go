package main

import (
	"fmt"
	"net/http"
	"strings"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "requested")
	var headers []string
	for k, v := range r.Header {
		headers = append(headers, fmt.Sprintf("%v: %v", k, v))
	}
	fmt.Fprintf(w, strings.Join(headers, "\n"))
}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
}
