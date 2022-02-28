package main

import (
	"fmt"
	"log"

	"example.com/greetings"
)

func main() {
	// Set properties of predefined Logger, including
	// the log entry prefix and a flag to disable printing
	// the time, source file, and line number.
	log.SetPrefix("greetings: ")
	log.SetFlags(0)
	// A slice of names.
	name := []string{"Gladys", "Samantha", "Darrin"}
	// Get a greeting message and print it.
	message, err := greetings.Hellos(name)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(message)
}
