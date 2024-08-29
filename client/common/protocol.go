package common

import "fmt"

const bytesOfContentLength = 4

func readContentLength(socket SocketTCP) (uint32, error) {
	bufferOfContentLength := make([]byte, bytesOfContentLength)
	if err := socket.Receive(bufferOfContentLength); err != nil {
		return 0, err
	}
	return ntohl(bufferOfContentLength), nil
}

func writeContentLength(data string) string {
	contentLength := htonl(uint32(len(data)))
	return fmt.Sprintf("%s%s", string(contentLength), data)
}

type Protocol struct {
	clientId string
}

func NewProtocol(clientId string) *Protocol {
	return &Protocol{
		clientId: clientId,
	}
}

func (p *Protocol) RegisterBet(socket SocketTCP, messageId string, message BetMessage) (*PacketResponse, error) {
	if err := p.sendBetRegister(socket, messageId, message); err != nil {
		log.Debugf("action: after_send_bet")
		return nil, err
	}
	return p.receiveBetRegisterResponse(socket)
}

func (p *Protocol) sendBetRegister(socket SocketTCP, messageId string, message BetMessage) error {
	packet := Packet{
		Command:   "REGISTER_BET",
		ClientId:  p.clientId,
		MessageId: messageId,
		Data:      message.Serialize(),
	}
	data := writeContentLength(packet.Serialize())
	return socket.Send([]byte(data))
}

func (p *Protocol) receiveBetRegisterResponse(socket SocketTCP) (*PacketResponse, error) {
	contentLength, err := readContentLength(socket)
	if err != nil {
		return nil, err
	}

	bufferOfDataResponse := make([]byte, contentLength)
	if err := socket.Receive(bufferOfDataResponse); err != nil {
		return nil, err
	}
	packetResponse := DeserializePacketResponse(string(bufferOfDataResponse))
	return packetResponse, nil
}
