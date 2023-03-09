// client that connects to the server and sends a message through a Unix domain socket

package main

import (
	"fmt"
	"net"
	"os"
)

func main() {
	// connect to the server
	conn, err := net.Dial("unix", "/tmp/uds_socket")
	if err != nil {
		fmt.Println("Error connecting:", err.Error())
		os.Exit(1)
	}
	defer conn.Close()

	// send a message to the server
	_, err = conn.Write([]byte("Hello, Unix domain socket!"))
	if err != nil {
		fmt.Println("Error writing:", err.Error())
		os.Exit(1)
	}
}