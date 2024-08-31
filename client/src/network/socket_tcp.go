package network

import (
	"bufio"
	"net"
)

type SocketTCP struct {
	address        string
	connection     net.Conn
	bufferedWriter *bufio.Writer
	bufferedReader *bufio.Reader
}

func NewSocketTCP(address string) *SocketTCP {
	return &SocketTCP{address: address}
}

func (s *SocketTCP) DeleteSocketTCP() {
	if s.connection != nil {
		s.connection.Close()
		s.connection = nil
	}
}

func (s *SocketTCP) Connect() error {
	connection, err := net.Dial("tcp", s.address)
	s.connection = connection
	s.bufferedWriter = bufio.NewWriter(connection)
	s.bufferedReader = bufio.NewReader(connection)
	return err
}

func (s *SocketTCP) Send(data []byte) error {
	remainingBytes := len(data)
	for remainingBytes > 0 {
		n, err := s.bufferedWriter.Write(data)
		remainingBytes -= n
		data = data[n:]
		if err != nil {
			return err
		}
	}
	return s.bufferedWriter.Flush()
}

func (s *SocketTCP) Receive(buffer []byte) error {
	remainingBytes := len(buffer)
	for remainingBytes > 0 {
		n, err := s.bufferedReader.Read(buffer)
		remainingBytes -= n
		buffer = buffer[n:]
		if err != nil {
			return err
		}
	}
	return nil
}
