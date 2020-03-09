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
	v.BindEnv("id")
	v.BindEnv("server", "address")
	v.BindEnv("loop", "period")
	v.BindEnv("loop", "lapse")

	// Parse time.Duration variables and return an error
	// if those variables cannot be parsed
	if _, err := time.ParseDuration(v.GetString("loop_lapse")); err != nil {
		return nil, errors.Wrapf(
			err,
			"Could not parse CLI_LOOP_LAPSE env var as time.Duration.",
		)
	}

	if _, err := time.ParseDuration(v.GetString("loop_period")); err != nil {
		return nil, errors.Wrapf(
			err,
			"Could not parse CLI_LOOP_PERIOD env var as time.Duration.",
		)
	}

	return v, nil
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func CreateClientSocket(v *viper.Viper) net.Conn {
	conn, err := net.Dial("tcp", v.GetString("server_address"))
	if err != nil {
		log.Fatalf(
			"[CLIENT %v] Could not connect to server. Error: %s",
			v.GetString("id"),
			err,
		)
	}
	return conn
}

// StartClientLoop Send messages to
func StartClientLoop(v *viper.Viper) {
	loopLapse := v.GetDuration("loop_lapse")
	loopPeriod := v.GetDuration("loop_period")
	clientID := v.GetString("id")

	for start := time.Now(); time.Since(start) < loopLapse; {
		// Create a new client socket in every for iteration
		clientSocket := CreateClientSocket(v)
		fmt.Fprintf(
			clientSocket,
			"[CLIENT %v] Message sent\n",
			clientID,
		)
		msg, err := bufio.NewReader(clientSocket).ReadString('\n')

		if err != nil {
			log.Errorf(
				"[CLIENT %v] Error reading from socket. Aborting.",
				clientID,
			)
			clientSocket.Close()
			return
		}

		log.Infof("[CLIENT %v] Message from server: %v", clientID, msg)
		time.Sleep(loopPeriod)
		clientSocket.Close()
	}

	log.Infof("[CLIENT %v] Main loop finished", clientID)
}

func main() {
	v, err := InitConfig()
	if err != nil {
		log.Fatalf("%s", err)
	}

	StartClientLoop(v)
}
