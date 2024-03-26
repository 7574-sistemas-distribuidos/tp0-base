package common

import (
	"bufio"
	"fmt"
	"net"
	"os"
    "os/signal"
    "syscall"
	"time"
	log "github.com/sirupsen/logrus"
)

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopLapse     time.Duration
	LoopPeriod    time.Duration
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
func (c *Client) StartClientLoop(bet Bet) {

	// Create the connection the server 
	c.createClientSocket()
    
	// Create write and read buffer from the socket
	writer := bufio.NewWriter(c.conn)
	scanner := bufio.NewScanner(c.conn)
	
	c.HandleSIGTERM()

	total_bets := 1
	bets_sent := 0

loop:
	for ;  ; {
		
		message := SerializeBet(bet)
	
		_, err := writer.Write(message)
		if err != nil {
			log.Errorf(
				"action: send_message | result: fail | client_id: %v | error: %v", 
				c.config.ID, 
				err,
			)
			return
		}
	
		// Flush the bufio.Writer to ensure that all data is sent to the socket
		err = writer.Flush()
		if err != nil {
			fmt.Println("Error flushing the bufio.Writer:", err)
			return
		}
		
		// Use the scanner to read the following line of the data stream
		if !scanner.Scan() {
			err := scanner.Err()
			if err != nil {
				log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
					c.config.ID,
					err,
				)
				return
			}
		}

		msg_received := scanner.Text()
	
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
		log.Infof("action: bet_sent | result: success | dni: %v | numero: %v",
            bet.Document,
            bet.Number,
        )

		bets_sent++

		if bets_sent == total_bets {
			break loop
		}

		// Wait a time between sending one message and the next one
		time.Sleep(c.config.LoopPeriod)
	}

	writer.Flush()
    scanner = nil
	c.conn.Close()
	log.Infof("action: finished | result: success | client_id: %v | bets_sent: %v", c.config.ID, bets_sent)
}
