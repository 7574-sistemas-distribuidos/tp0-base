package network

import "encoding/binary"

func Htonl(value uint32) []byte {
	sizeBytes := make([]byte, 4)
	binary.BigEndian.PutUint32(sizeBytes, value)
	return sizeBytes
}

func Ntohl(value []byte) uint32 {
	return binary.BigEndian.Uint32(value)
}
