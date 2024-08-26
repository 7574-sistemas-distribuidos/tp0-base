package common

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopAmount    int
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
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}
	c.conn = conn
	return nil
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	signalChannel := c.setGracefulShutdown()
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed
	join := make(chan struct{}, 1)
	msgID := 1
	for msgID <= c.config.LoopAmount {
		go c.processClient(msgID, join)

		select {
		case <-signalChannel:
			c.releaseResources()
			return
		case <-join:
			msgID++
		}
	}
	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}

func (c *Client) setGracefulShutdown() chan os.Signal {
	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, syscall.SIGTERM)
	return signalChannel
}

func (c *Client) processClient(msgID int, join chan struct{}) {
	// Create the connection the server in every loop iteration. Send an
	c.createClientSocket()

	// TODO: Modify the send to avoid short-write
	fmt.Fprintf(
		c.conn,
		"[CLIENT %v] Message N°%v\n",
		c.config.ID,
		msgID,
	)
	msg, err := bufio.NewReader(c.conn).ReadString('\n')
	c.releaseConn()

	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}

	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		c.config.ID,
		msg,
	)

	// Wait a time between sending one message and the next one
	time.Sleep(c.config.LoopPeriod)
	join <- struct{}{}
}

func (c *Client) releaseResources() {
	log.Infof("action: releasing_resources | result: in_progress | client_id: %v", c.config.ID)
	c.releaseConn()
	log.Infof("action: releasing_resources | result: success | client_id: %v", c.config.ID)
}

func (c *Client) releaseConn() {
	if c.conn != nil {
		c.conn.Close()
		c.conn = nil
	}
}
