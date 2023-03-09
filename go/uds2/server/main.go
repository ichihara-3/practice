// server that listens on a Unix domain socket


package main

import (
	"fmt"
	"net"
	"os"
)

func main() {
	// remove the socket file if it exists
	os.Remove("/tmp/uds_socket")

	// listen on a Unix domain socket
	l, err := net.Listen("unix", "/tmp/uds_socket")
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}

	fmt.Println("Listening on /tmp/uds_socket")

	// accept connection on socket
	conn, err := l.Accept()
	if err != nil {
		fmt.Println("Error accepting: ", err.Error())
		os.Exit(1)
	}

	// read in input from the connection
	buf := make([]byte, 1024)
	reqLen, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}
	fmt.Printf("Received data: %v", string(buf[:reqLen]))
}

// 