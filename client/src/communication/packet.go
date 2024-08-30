package communication

import (
	"fmt"
	"strings"
)

const newLine = "\n"
const tagValueSeparator = ": "

type Packet struct {
	Command   string
	ClientId  string
	MessageId string
	Data      string
}

func (p *Packet) Serialize() string {
	command := fmt.Sprintf("COMMAND%s%s%s", tagValueSeparator, p.Command, newLine)
	clientId := fmt.Sprintf("CLIENT_ID%s%s%s", tagValueSeparator, p.ClientId, newLine)
	messageId := fmt.Sprintf("MESSAGE_ID%s%s%s", tagValueSeparator, p.MessageId, newLine)
	header := command + clientId + messageId
	body := p.Data
	packet := header + newLine + body
	return packet
}

type PacketResponse struct {
	status string
}

func DeserializePacketResponse(data string) *PacketResponse {
	response := strings.Split(data, newLine)
	statusHeader := strings.Split(response[0], tagValueSeparator)
	return &PacketResponse{status: statusHeader[1]}
}
