package common

import (
	"bufio"
	"fmt"
)

// Send bets to the server
func SendMessage(id int, writer *bufio.Writer, message []byte) error {
	bytes_sent, err := writer.Write(message)
	if err != nil {
		return fmt.Errorf("action: send_message | result: fail | client_id: %v | error: %v", id, err)
	}

	// Flush the bufio.Writer to ensure that all data is sent to the socket
	err = writer.Flush()
	if err != nil {
		return fmt.Errorf("Error flushing the bufio.Writer: %v", err)
	}

	if bytes_sent != len(message) {
		return fmt.Errorf("Error not all bytes were sent: %v / %v", bytes_sent, len(message))
	}

	return nil
}

// Receives an ACK from the server
func ReceiveMessage(id int, scanner *bufio.Scanner) (string, error) {
	// Use the scanner to read the following line of the data stream
	if !scanner.Scan() {
		err := scanner.Err()
		if err != nil {
			return "", fmt.Errorf("action: receive_message | result: fail | client_id: %v | error: %v", id, err)
		}
	}

	return scanner.Text(), nil
}