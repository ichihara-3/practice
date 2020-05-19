package main

import (
	"fmt"
	"log"
	"net"
)

func handleUdpConnection(conn net.UDPConn) {
	defer conn.Close()
	buf := make([]byte, 1024)

	for {
		n, addr, err := conn.ReadFromUDP(buf)
		if err != nil {
			log.Fatal(err)
		}
		if n == 0 {
			break
		}

		fmt.Print(string(buf[:n]))

		_, err = conn.WriteToUDP(buf[:n], addr)
		if err != nil {
			log.Fatal(err)
		}
	}
}

func main() {
	addr, err := net.ResolveUDPAddr("udp", ":7")
	if err != nil {
		log.Fatal(err)
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	handleUdpConnection(*conn)
}
