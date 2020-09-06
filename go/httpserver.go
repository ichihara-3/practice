package main

import (
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	defer log(w, r)
	fmt.Fprintln(w, "hello")
}

type CountHandler struct {
	mu sync.Mutex
	n  int
}

func (c *CountHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	defer log(w, r)
	c.mu.Lock()
	defer c.mu.Unlock()
	c.n++
	fmt.Fprintf(w, "count: %v\n", c.n)
}

func log(w http.ResponseWriter, r *http.Request) {
	now := time.Now()
	uri := r.RequestURI
	var headers []string
	for k, v := range r.Header {
		headers = append(headers, fmt.Sprintf("%v: %v", k, v))
	}
	fmt.Printf("%v\t%s\tHeaders: %s\n", now, uri, strings.Join(headers, ","))
}

func main() {
	http.HandleFunc("/", handler)
	http.Handle("/count", new(CountHandler))
	http.ListenAndServe(":8080", nil)
}
