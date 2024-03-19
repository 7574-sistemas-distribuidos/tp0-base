package common

import (
	"bufio"
	"fmt"
	"net"
	"time"
	"os"
    "os/signal"
    "syscall"
	"encoding/binary"

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


type LotteryMsg struct {
	birth_date    time.Time
	dni           uint32
	lotteryNumber uint32
	name          string
	lastName      string
}

//NOMBRE=Santiago Lionel, APELLIDO=Lorca, DOCUMENTO=30904465, NACIMIENTO=1999-03-17 y NUMERO=7574

func LotteryMsgFromEnv() *LotteryMsg{
	const SAMPLE_DATE = "2006-02-22"
	birth_date := os.Getenv("NACIMIENTO")
	fmt.Println("Env:", birth_date)
	fecha, err := time.Parse(SAMPLE_DATE, birth_date)
	fmt.Println("Fecha:", fecha)

    if err != nil {
        fmt.Println("Error al analizar la fecha:", err)
        return nil
    }
	//dni: os.Getenv("DOCUMENTO"),
	//lotteryNumber: os.Getenv("NUMERO"),
	//name: os.Getenv("NOMBRE"),
	//lastName: os.Getenv("APELLIDO"),
	/*
	lotteryMsg := &LotteryMsg{
		birth_date: os.Getenv("DOCUMENTO"),
		dni: os.Getenv("NACIMIENTO"),
		lotteryNumber: os.Getenv("NUMERO"),
		name: os.Getenv("NOMBRE"),
		lastName: os.Getenv("APELLIDO"),
	}
	return lotteryMsg
	*/
	return nil
}

func dateToBytes(date time.Time) []byte {
	var data []byte

	data = append(data, byte(date.Day()))
	data = append(data, byte(date.Month()))
	year_bytes := make([]byte, 2)
	binary.BigEndian.PutUint16(year_bytes, uint16(date.Year()))
	data = append(data, year_bytes...)
	return data
}

func lotterryMsgToBytes(msg LotteryMsg) []byte {
	const MAX_NAME_LEN = 127
	var data []byte = dateToBytes(msg.birth_date)

	dni_bytes := make([]byte, 4)
	binary.BigEndian.PutUint32(dni_bytes, msg.dni)
	data = append(data, dni_bytes...)

	lottery_number_bytes := make([]byte, 4)
	binary.BigEndian.PutUint32(lottery_number_bytes, msg.lotteryNumber)
	data = append(data, lottery_number_bytes...)

	full_name := truncateString(msg.name, MAX_NAME_LEN) + ";" + truncateString(msg.lastName, MAX_NAME_LEN)
	data = append(data, byte(len(full_name)))
	data = append(data, []byte(full_name)...)
	return data
}

func truncateString(str string, maxLength int) string {
	if len(str) > maxLength {
		return str[:maxLength]
	}
	return str
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

	//LotteryMsgFromEnv()
	//return
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
		default:
		}

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
		msgID++
		c.conn.Close()

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

		select {
		case <-sigs:
			log.Infof("catcheado")
			break loop
		}
	}

	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}
