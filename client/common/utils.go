package common

import (
	//"bufio"
	"net"
)

// Sends bytes until all of them are sent, or a failure occurs in which case error 
// is returned. nil is return on succes
func send_all(conn net.Conn, byte_array []byte) error{
	for{
		if len(byte_array) <= 0{
			return nil
		}
		sent, err := conn.Write(byte_array)
		if err != nil {
			return err
		}
		byte_array = byte_array[sent:]
	}
}

// Receives bytes until n bytes have been received. If cannot receive n bytes error is returned
func recv_exactly(conn net.Conn, n uint32) ([]byte, error){
	var buffer []byte
	for{
		if n <= 0{
			return buffer, nil
		}
		byte_array := make([]byte, n)
		bytes_read, err := conn.Read(byte_array)
    	if err != nil {
			return nil, err
    	}
        buffer = append(buffer, byte_array...)
        n -= uint32(bytes_read)
	}
}