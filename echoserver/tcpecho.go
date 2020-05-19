package main

import (
	"fmt"
	"log"
	"net"
)

func handleConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if n == 0 {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(string(buf[:n]))
		_, err = conn.Write(buf[:n])
		if err != nil {
			log.Fatal(err)
		}
	}
}

func main() {
	ln, err := net.Listen("tcp", ":7")
	if err != nil {
		log.Fatal(err)
	}
	defer ln.Close()
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatal(err)
		}
		go handleConnection(conn)
	}

}
