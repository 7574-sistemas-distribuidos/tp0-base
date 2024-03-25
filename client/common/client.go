package common

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/signal"
	"strconv"
	"strings"
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

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	// autoincremental msgID to identify every message sent
	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, syscall.SIGTERM)

	filename := "agency-" + c.config.ID + ".csv"
	file, err := os.Open(filename)
	if err != nil {
		log.Fatalf("Failed to open file: %s", err)
	}
	defer file.Close()
	reader := bufio.NewReader(file)

	// Send messages if the loopLapse threshold has not been surpassed
	for timeout := time.After(c.config.LoopLapse); ; {
		select {
		case <-timeout:
			log.Infof("action: timeout_detected | result: success | client_id: %v",
				c.config.ID,
			)
			return

		case <-sigchan:
			log.Infof("CLIENTE RECIBIO SIGTERM")
			c.conn.Close()
			return

		default:
		}

		// Create the connection the server in every loop iteration. Send an

		c.createClientSocket()

		// SENDING
		batch_size := 02
		for i := 0; i < batch_size; i++ {
			msg_to_sv := fmt.Sprintf("%v", batch_size)
			msg_to_sv += create_message(c, reader)
			send_message(c, c.conn, msg_to_sv)
		}

		//READING
		sv_answer := read_message(c, c.conn)
		answer := strings.Split(sv_answer, " ")
		if answer[0] == "err" {
			c.conn.Close()
			return
		}
		// Wait a time between sending one message and the next one
		time.Sleep(c.config.LoopPeriod)
		c.conn.Close()

		log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
	}
}

func read_message(c *Client, conn net.Conn) string {
	bytes_read := 0
	reader := bufio.NewReader(conn)
	recv, err := reader.ReadString('\n')
	verify_recv_error(c, err)
	bytes_read += len(recv)

	header, err := strconv.Atoi(recv[:2])
	for bytes_read < header+2 {
		read, err := reader.ReadString('\n')
		verify_recv_error(c, err)
		bytes_read += len(read)
	}
	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		c.config.ID,
		recv,
	)
	// Return the message without the header
	return recv[3:]
}

func verify_recv_error(c *Client, err error) {
	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}
}

func send_message(c *Client, conn net.Conn, msg string) {
	bytes_sent := 0
	log.Infof("ABOUT TO SEND: msg: %v", msg)
	for bytes_sent < len(msg) {
		bytes, err := fmt.Fprintf(
			conn,
			msg[bytes_sent:],
		)
		if err != nil {
			log.Errorf("action: send_message | result: fail | client_id: %v | error: %v",
				c.config.ID,
				err,
			)
			conn.Close()
			return
		}
		bytes_sent += bytes
	}
}

func read_csv_line(reader *bufio.Reader) string {
	line, err := reader.ReadString('\n')
	if err != nil {
		log.Fatalf("Failed to read line: %s", err)
		return ""
	}
	return line
}

func create_message(c *Client, reader *bufio.Reader) string {
	msg_to_sv := ""

	line := read_csv_line(reader)
	if line == "" {
		return "err"
	}
	fields := strings.Split(line, ",")
	fields[4] = strings.TrimSuffix(fields[4], "\n")
	fields[4] = strings.TrimSuffix(fields[4], "\r")
	msg_to_sv += fmt.Sprintf("|AGENCIA %v|NOMBRE %v|APELLIDO %v|DNI %v|NACIMIENTO %v|NUMERO %v|$", c.config.ID, fields[0], fields[1], fields[2], fields[3], fields[4]) //PONER CONSTANTES
	//header := fmt.Sprintf("%v ", len(msg_to_sv))
	//msg_to_sv = header + msg_to_sv
	return msg_to_sv
}
