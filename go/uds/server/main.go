// server that creates a unix domain socket and listens for connections
package main

import (
	"fmt"
	"io"
	"net"
	"os"
)

func main() {
	file := "/tmp/uds.sock"
	// remove the socket file if it already exists
	os.Remove(file)

	// create a unix domain socket
	l, err := net.Listen("unix", file)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	// close the socket when the program exits
	defer l.Close()

	fmt.Println("Listening on " + file)
	for {
		// accept a connection
		conn, err := l.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		// handle the connection
		go handleRequest(conn)
	}
}

func handleRequest(conn net.Conn) {
	// read the request
	buf := make([]byte, 10)
	fmt.Printf("Received data: ")
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err != io.EOF {
				fmt.Println("Error reading:", err.Error())
				return
			}
			break
		}
		fmt.Printf("%v", string(buf[:n]))
	}
}