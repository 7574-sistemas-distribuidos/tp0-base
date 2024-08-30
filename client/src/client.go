package common

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/src/communication"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/src/network"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopAmount    int
	LoopPeriod    time.Duration
	Name          string
	LastName      string
	IdNumber      string
	Birthdate     string
	BetNumber     string
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	socket *network.SocketTCP
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
func (c *Client) createSocket() error {
	socket := network.NewSocketTCP(c.config.ServerAddress)
	err := socket.Connect()

	if err != nil {
		log.Criticalf("action: connect | result: fail | client_id: %v | error: %v", c.config.ID, err)
	}
	c.socket = socket
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
	// Create the connection the server in every loop iteration.
	c.createSocket()
	defer c.destroySocket()

	protocol := communication.NewProtocol(c.config.ID, *c.socket)
	betContent := communication.BetContent{
		Name:      c.config.Name,
		LastName:  c.config.LastName,
		IdNumber:  c.config.IdNumber,
		Birthdate: c.config.Birthdate,
		BetNumber: c.config.BetNumber,
	}
	msg, err := protocol.RegisterBet(fmt.Sprintf("%v", msgID), betContent)

	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}

	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		c.config.ID,
		*msg,
	)

	// Wait a time between sending one message and the next one
	time.Sleep(c.config.LoopPeriod)
	join <- struct{}{}
}

func (c *Client) releaseResources() {
	log.Infof("action: releasing_resources | result: in_progress | client_id: %v", c.config.ID)
	c.destroySocket()
	log.Infof("action: releasing_resources | result: success | client_id: %v", c.config.ID)
}

func (c *Client) destroySocket() {
	c.socket.DeleteSocketTCP()
}
