package communication

import (
	"fmt"
	"strings"
)

const newLine = "\n"
const headerContentSeparator = "\n\n"
const tagValueSeparator = ": "

type Packet struct {
	Command   string
	ClientId  string
	MessageId string
	Content   string
}

func (p *Packet) Serialize() string {
	command := fmt.Sprintf("COMMAND%s%s%s", tagValueSeparator, p.Command, newLine)
	clientId := fmt.Sprintf("CLIENT_ID%s%s%s", tagValueSeparator, p.ClientId, newLine)
	messageId := fmt.Sprintf("MESSAGE_ID%s%s%s", tagValueSeparator, p.MessageId, newLine)
	header := command + clientId + messageId
	content := p.Content
	packet := header + newLine + content
	return packet
}

type PacketResponse struct {
	Status  string
	Content string
}

func DeserializePacketResponse(data string) *PacketResponse {
	response := strings.Split(data, headerContentSeparator)
	headers := response[0]
	content := response[1]
	status := ""
	for _, header := range strings.Split(headers, newLine) {
		line := strings.Split(header, tagValueSeparator)
		tag := line[0]
		value := line[1]
		if tag == "STATUS" {
			status = value
		}
	}
	return &PacketResponse{Status: status, Content: content}
}
