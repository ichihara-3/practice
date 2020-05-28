package main

import (
	"log"
	"net/http"
)

func main() {
	http.Handle("/", http.FileServer(http.Dir("static")))

	if err := http.ListenAndServe(":10080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
