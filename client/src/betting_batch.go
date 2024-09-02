package common

import (
	"fmt"
	"time"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/src/communication"
)

const maxDataToSend = 8 * 1024

type BettingBatch struct {
	bettingFileReader *BettingFileReader
	maxBatchSize      int
	protocol          communication.Protocol
	bytesRead         int
	outgoingBets      []communication.BetContent
	clientConfig      ClientConfig
	msgID             int
}

func NewBettingBatch(filename string, maxBatchSize int, c ClientConfig, protocol communication.Protocol) (*BettingBatch, error) {
	bettingFileReader, err := NewBettingFileReader(filename)
	if err != nil {
		return nil, err
	}
	bettingBatch := BettingBatch{
		bettingFileReader: bettingFileReader,
		maxBatchSize:      maxBatchSize,
		protocol:          protocol,
		bytesRead:         0,
		outgoingBets:      make([]communication.BetContent, 0),
		clientConfig:      c,
		msgID:             1,
	}
	return &bettingBatch, nil
}

func (bb *BettingBatch) DeleteBettingBatch() error {
	return bb.bettingFileReader.DeleteBettingFileReader()
}

func (bb *BettingBatch) RegisterBets() (string, error) {
	for {
		serializedBet := bb.bettingFileReader.ReadBet()

		if err := bb.bettingFileReader.Error(); err != nil {
			log.Debugf("accion: file_read | resultado: fail | cliente_id: %v | error: %v", bb.clientConfig.ID, err)
			bb.Flush()
			return "", err
		}

		if bb.bettingFileReader.IsEOF() {
			log.Debugf("accion: file_read | resultado: success | cliente_id: %v", bb.clientConfig.ID)
			bb.Flush()
			return "", nil
		}

		bb.processBet(serializedBet)
	}
}

func (bb *BettingBatch) processBet(serializedBet string) {
	currentBytesRead := len(serializedBet)
	bet := communication.DeserializeBetContent(serializedBet)

	if len(bb.outgoingBets) < bb.maxBatchSize && bb.bytesRead+currentBytesRead < maxDataToSend {
		bb.outgoingBets = append(bb.outgoingBets, *bet)
		bb.bytesRead += currentBytesRead
	} else {
		bb.registerBets()
		bb.outgoingBets = bb.outgoingBets[:0]
		bb.outgoingBets = append(bb.outgoingBets, *bet)
		bb.bytesRead = currentBytesRead
	}
}

func (bb *BettingBatch) Flush() {
	if len(bb.outgoingBets) > 0 {
		bb.registerBets()
	}
	bb.closeConnection()
}

func (bb *BettingBatch) registerBets() {
	msg, err := bb.protocol.RegisterBets(fmt.Sprintf("%v", bb.msgID), bb.outgoingBets)
	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v", bb.clientConfig.ID, err)
		return
	}

	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v", bb.clientConfig.ID, *msg)
	time.Sleep(bb.clientConfig.LoopPeriod)
	bb.msgID++
}

func (bb *BettingBatch) closeConnection() {
	err := bb.protocol.CloseConnection(fmt.Sprintf("%v", bb.msgID))
	if err != nil {
		log.Debugf("action: close_connection | result: fail | client_id: %v | error: %v", bb.clientConfig.ID, err)
	}
}
