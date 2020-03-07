package main

import (
	"bufio"
	"fmt"
	"net"
	"time"

	"github.com/pkg/errors"
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
	if _, err := time.ParseDuration(v.GetString("loop_lapse")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_LAPSE env var as time.Duration.")
	}

	if _, err := time.ParseDuration(v.GetString("loop_period")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_PERIOD env var as time.Duration.")
	}

	return v, nil
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func CreateClientSocket(v *viper.Viper) net.Conn {
	conn, err := net.Dial("tcp", v.GetString("server_address"))
	if err != nil {
		log.Fatalf("Could not connect to server. Error: %s", err)
	}
	return conn
}

// StartClientLoop Send messages to
func StartClientLoop(v *viper.Viper, clientSocket net.Conn) {
	loopLapse := v.GetDuration("loop_lapse")
	loopPeriod := v.GetDuration("loop_period")

loop:
	for timeout := time.After(loopLapse); ; {
		select {
		case <-timeout:
			break loop
		default:
		}

		fmt.Fprintf(clientSocket, "This is a message from the client\n")
		message := bufio.NewReader(clientSocket)
		log.Infof("Message from server: %s", message)
		time.Sleep(loopPeriod)
	}

	clientSocket.Close()
}

func main() {
	v, err := InitConfig()
	if err != nil {
		log.Fatalf("%s", err)
	}

	clientSocket := CreateClientSocket(v)
	StartClientLoop(v, clientSocket)
}
