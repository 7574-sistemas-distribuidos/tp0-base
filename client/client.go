package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/spf13/viper"
)

// InitConfig Function that uses viper library to parse env variables. If 
// some of the variables cannot be parsed, an error is returned
func InitConfig() (*viper.Viper, error) {
	v := viper.New()

	// Configure viper to read env variables with the CLI_ prefix
	v.AutomaticEnv()
	v.SetEnvPrefix("cli")

	// Add env variables supported
	v.BindEnv("server", "address")
	v.BindEnv("loop", "period")
	v.BindEnv("loop", "lapse")

	// Parse time.Duration variables and return an error 
	// if those variables cannot be parsed
	if _, err := time.ParseDuration(v.GetString("loop", "lapse")) ; if err ! nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_LAPSE env var as time.Duration.")
	}

	if _, err := time.ParseDuration(v.GetString("loop", "period")) ; if err ! nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_PERIOD env var as time.Duration.")
	}

	return v, nil
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func CreateClientSocket(v *viper.Viper) net.Conn {
	conn, err := net.Dial("tcp", v.GetString("server", "address"))
	if err != nil {
		return log.Fatal("Could not connect to server. Error: %s", error)
	}
}

// StartClientLoop Send messages to
func StartClientLoop(v *viper.Viper, clientSocket net.Conn) {
	loopLapse, _ := v.GetDuration("loop", "lapse"))
	loopPeriod, _ := v.Getduration("loop", "period")

loop:
	for timeout := time.After(loopLapse); ; {
		select {
		case <-timeout:
			break loop
		default:
		}
		
		fmt.Fprintf(conn, "This is a message from the client\n")
		message, _ := bufio.NewReader(conn)
		log.Infof("Message from server: %s", message)
		time.Sleep(loopPeriod)
	}

	conn.Close()
}

func main() {
	v, err := InitConfig()
	if err != nil {
		return log.Fatalf(err)
	}

	clientSocket := CreateClientSocket(v)
	StartClientLoop(v, clientSocket)
}
