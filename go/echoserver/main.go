package main

import (
	"flag"
	"io"
	"log"
	"net"
)

func main() {
	var t = flag.String("t", "tcp", "a type to launch the server: tcp or udp")
	flag.Parse()
	if *t == "tcp" {
		tcpServer()
	} else if *t == "udp" {
		udpServer()
	} else {
		log.Fatalf("type must be 'tcp' or 'udp', got %s.", *t)
	}
}

func tcpServer() {
	ln, err := net.Listen("tcp", ":7")
	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatal(err)
		}
		buf := make([]byte, 1024)
		for {
			n, err := conn.Read(buf)
			if err != nil {
				if err == io.EOF {
					break
				} else {
					log.Fatal(err)
				}
			}
			if n == 0 {
				break
			}
			conn.Write(buf[:n])
		}
	}
}

func udpServer() {
	addr := net.UDPAddr{
		IP:   net.IPv4(127, 0, 0, 1),
		Port: 7,
	}
	conn, err := net.ListenUDP("udp", &addr)
	if err != nil {
		log.Fatal(err)
	}
	buf := make([]byte, 1024)
	for {
		n, addr, err := conn.ReadFromUDP(buf)
		if err != nil {
			if err == io.EOF {
				break
			} else {
				log.Fatal(err, addr)
			}
		}
		if n == 0 {
			break
		}
		conn.WriteToUDP(buf[:n], addr)
	}
}
