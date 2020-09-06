package main

import (
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	var status int
	if r.URL.Path != "/" {
		status = http.StatusNotFound
	} else {
		status = http.StatusOK
	}
	defer log(w, r, status)
	w.WriteHeader(status)
	fmt.Fprintln(w, "hello")
}

type CountHandler struct {
	mu sync.Mutex
	n  int
}

func (c *CountHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	defer log(w, r, http.StatusOK)
	c.mu.Lock()
	defer c.mu.Unlock()
	c.n++
	fmt.Fprintf(w, "count: %v\n", c.n)
}

func log(w http.ResponseWriter, r *http.Request, status int) {
	now := time.Now()
	uri := r.RequestURI
	var headers []string
	for k, v := range r.Header {
		headers = append(headers, fmt.Sprintf("%v: %v", k, v))
	}
	fmt.Printf("%v\t%s\t%d\tHeaders: %s\n", now, uri, status, strings.Join(headers, ","))
}

func main() {
	http.HandleFunc("/", handler)
	http.Handle("/count", new(CountHandler))
	http.ListenAndServe(":8080", nil)
}
