package main

import (
	"flag"
	"net/http"
	"runtime"
	"testing"
)

var (
	parallel = flag.Int("p", runtime.NumCPU(), "Number of parallel requests")
	target   = flag.String("t", "http://localhost:8080", "Target URL")
)

func main() {
	testing.Benchmark(BenchmarkGet)
}

func BenchmarkGet(b *testing.B) {
	b.SetParallelism(*parallel)
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			Get(*target)
		}
	})
}

func Get(url string) {
	_, err := http.Get(url)
	if err != nil {
		panic(err)
	}
}
