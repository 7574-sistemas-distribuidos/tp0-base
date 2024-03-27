package common

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"net"
	"os"
    "os/signal"
    "syscall"
	"strconv"
	"time"
	"path/filepath"
	log "github.com/sirupsen/logrus"
)

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopLapse     time.Duration
	LoopPeriod    time.Duration
	ChunkSize     int
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Fatalf(
	        "action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}
	c.conn = conn
	return nil
}

func (c *Client) CloseClient(writer *bufio.Writer, reader *bufio.Reader) {

	// Release resources
	err := writer.Flush()
	if err != nil {
		log.Errorf("Error flushing the bufio.Writer: %v", err)
	}
	reader = nil

	c.conn.Close()
}

func (c *Client) HandleSIGTERM() {
    // Make a channel to receive SIGTERM 
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGTERM)

    // Routine in the background to handle SIGTERM signal
    go func() {
        <-sigCh
        log.Println("SIGTERM received, shutting down gracefully")
        
        if c.conn != nil {
            c.conn.Close()
        }
        os.Exit(0)
    }()
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {

	c.HandleSIGTERM()

	// Create the connection the server 
	c.createClientSocket()

	// Open file
	fileName := "agency-" + c.config.ID + ".csv"
	dataDir := filepath.Join("/.data") 
	filePath := filepath.Join(dataDir, fileName)
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Printf("Error opening the file: %v\n", err)
		return
	}
	defer file.Close()

	// New reader
	csv_reader := csv.NewReader(file)
    
	// Create write and read buffer from the socket
	writer := bufio.NewWriter(c.conn)
	reader := bufio.NewReader(c.conn)

	defer c.CloseClient(writer, reader)

	bets_sent := 0

	id, err := strconv.Atoi(c.config.ID)
	if err != nil {
		log.Errorf(
			"Error converting id to an integer %v", err, 
		)
		return 
	}

	// First msg: send the id of the client
	idBytes := EncodeInt(id)

	err = SendMessage(id, writer, idBytes)
	if err != nil {
		fmt.Println("%v", err)
		return
	}

	// Send messages if the loopLapse threshold has not been surpassed
	for {

		bets, err := ProcessCSV(csv_reader, c.config.ChunkSize, id)
		if err != nil {
			fmt.Println("%v", err)
			return
		}

		message, err := SerializeBets(bets)
		if err != nil {
			fmt.Println("%v", err)
			return
		}

		err = SendMessage(id, writer, message)
		if err != nil {
			fmt.Println("%v", err)
			return
		}

		msg_received, err := ReceiveConfirmation(id, reader)
		if err != nil {
			fmt.Println("%v", err)
			return
		}

		if err != nil {
			log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
                c.config.ID,
				err,
			)
			return
		}
		log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
            c.config.ID,
            msg_received,
        )

		chunkSize := len(bets)

		bets_sent = bets_sent + chunkSize

		log.Infof("action: bets_sent | result: success | total_bets_sent: %v | bets_sent: %v ",
			bets_sent,
			chunkSize,
		)

		// EOF was reached
		if chunkSize != c.config.ChunkSize {
			err = SendNoMoreBets(id, writer)
			if err != nil {
				fmt.Println("%v", err)
				return
			}
			break
		}

		// Wait a time between sending one message and the next one
		time.Sleep(c.config.LoopPeriod)
	}


	result, err := RequestResult(id, reader)
	if err != nil {
		fmt.Println("%v", err)
		return
	}

	log.Infof("action: winners_query | result: success | client_id: %v | tot_winners: %v", c.config.ID, result.TotalWinners)

	log.Infof("action: finished | result: success | client_id: %v | bets_sent: %v", c.config.ID, bets_sent)
}
