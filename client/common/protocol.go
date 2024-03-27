package common

import (
	"bufio"
	"fmt"
	"encoding/binary"
)

type Result struct {
    TotalWinners uint32
    Winners      []int32
}

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

// Indicate to the server that there are no more bets
func SendNoMoreBets(id int, writer *bufio.Writer) error {
	
	zeroBets := EncodeInt(0)

	_, err := writer.Write(zeroBets)
	if err != nil {
		return fmt.Errorf(
			"action: send_message | result: fail | client_id: %v | error: %v", 
			id, 
			err,
		)
	}

	// Flush the bufio.Writer to ensure that all data is sent to the socket
	err = writer.Flush()
	if err != nil {
		return fmt.Errorf("Error flushing the bufio.Writer: %v", err)
	}

	return nil
}

// Receives a confirmation from the server
func ReceiveConfirmation(id int, reader *bufio.Reader) (int, error) {

	var ackInt int32

	err := binary.Read(reader, binary.BigEndian, &ackInt)
	if err != nil {
		return 0, fmt.Errorf("action: receive_confirmation | result: fail | client_id: %v | error: %v", id, err)
	}

	// Check the data
	if ackInt != 1 {
		return 0, fmt.Errorf("action: receive_confirmation | result: fail | client_id: %v | error: invalid confirmation received", id)
	}

	return int(ackInt), nil
}

func RequestResult(id int, reader *bufio.Reader) (Result, error) {
    var result Result

    // Read the total number of winners
    if err := binary.Read(reader, binary.BigEndian, &result.TotalWinners); err != nil {
        return Result{}, fmt.Errorf("action: RequestResult | result: fail | client_id: %v | error receiving total winners: %v", id, err)
    }

    // Read the winner documents
    result.Winners = make([]int32, result.TotalWinners)
    for i := 0; i < int(result.TotalWinners); i++ {
        var document uint32
        if err := binary.Read(reader, binary.BigEndian, &document); err != nil {
            return Result{}, fmt.Errorf("action: RequestResult | result: fail | client_id: %v | error receiving winner document %v: %v", id, i+1, err)
        }
        result.Winners[i] = int32(document)
    }

    return result, nil
}