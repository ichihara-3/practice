// client that connects to the server and sends a message through unix domain socket
package main

import (
	"fmt"
	"net"
	"os"
)

func main() {
	// connect to the server
	conn, err := net.Dial("unix", "/tmp/uds.sock")
	if err != nil {
		fmt.Println("Error connecting:", err.Error())
		os.Exit(1)
	}
	defer conn.Close()

	// send a message
	_, err = conn.Write([]byte("Hello from client\n"))
	if err != nil {
		fmt.Println("Error writing:", err.Error())
	}
}
