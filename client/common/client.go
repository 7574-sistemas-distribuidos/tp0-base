package common

import (
	//"bufio"
	"net"
	"time"
	"os"
    "os/signal"
    "syscall"
	//"fmt"
	//"io"
	
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

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	
	const ANSWEAR_BYTES = 1
	// autoincremental msgID to identify every message sent
	msgID := 1
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGTERM)
	
	loop:
	// Send messages if the loopLapse threshold has not been surpassed
	for timeout := time.After(c.config.LoopLapse); ; {
		select {
			case <-timeout:
				log.Infof("action: timeout_detected | result: success | client_id: %v",
				c.config.ID,
				)
				break loop
			case <-sigs:
				break loop
			case <- time.After(c.config.LoopPeriod):
		}

		// Create the connection the server in every loop iteration. Send an
		c.createClientSocket()

		// TODO: Modify the send to avoid short-write
		bet := BetFromEnv()
		if bet == nil{
			log.Errorf("action: creando apuesta | result: fail | variables de entorno no inicializadas")
			c.conn.Close()
			return
		}
		err := send_all(c.conn, bet.ToBytes())
    	if err != nil {
        	log.Errorf("action: enviando apuesta | result: fail | client_id: %v | error: %v",
                c.config.ID,
				err,
			)
			c.conn.Close()
			return 
    	}
		//c.conn.Write(bet.BetToBytes())


		//msg, err := bufio.NewReader(c.conn).ReadString('\n')
		_,err = recv_exactly(c.conn, ANSWEAR_BYTES)
		msgID++
		c.conn.Close()

		if err != nil {
			log.Errorf("action: apuesta_enviada | result: fail | client_id: %v | error: %v",
                c.config.ID,
				err,
			)
			return
		}
		log.Infof("action: apuesta_enviada | result: success | dni: %v | numero: %v",
            bet.dni,
            bet.lotteryNumber,
        )
	}

	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}
	