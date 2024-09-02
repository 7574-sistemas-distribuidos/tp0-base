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
	ID             string
	ServerAddress  string
	LoopPeriod     time.Duration
	BatchMaxAmount int
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

func (c *Client) DeleteClient() {
	c.releaseResources()
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
	go c.processClient(join)

	select {
	case <-signalChannel:
		return
	case <-join:
		log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
	}
}

func (c *Client) setGracefulShutdown() chan os.Signal {
	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, syscall.SIGTERM)
	return signalChannel
}

func (c *Client) processClient(join chan struct{}) {
	c.createSocket()
	filename := fmt.Sprintf("/dataset/agency-%v.csv", c.config.ID)
	protocol := communication.NewProtocol(c.config.ID, *c.socket)
	bettingBatch, err := NewBettingBatch(filename, c.config.BatchMaxAmount, c.config, *protocol)
	defer bettingBatch.DeleteBettingBatch()
	if err != nil {
		log.Debugf("action: create_betting_batch | result: fail | client_id: %v | error: %v", c.config.ID, err)
	}

	bettingBatch.RegisterBets()
	join <- struct{}{}
}

func (c *Client) releaseResources() {
	log.Infof("action: releasing_resources | result: in_progress | client_id: %v", c.config.ID)
	c.socket.DeleteSocketTCP()
	log.Infof("action: releasing_resources | result: success | client_id: %v", c.config.ID)
}
