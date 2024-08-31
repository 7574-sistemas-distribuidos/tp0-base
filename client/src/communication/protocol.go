package communication

import (
	"fmt"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/src/network"
)

const bytesOfPacketLength = 4

type Protocol struct {
	clientId string
	socket   network.SocketTCP
}

func NewProtocol(clientId string, socket network.SocketTCP) *Protocol {
	return &Protocol{
		clientId: clientId,
		socket:   socket,
	}
}

func (p *Protocol) RegisterBet(messageId string, betContent BetContent) (*PacketResponse, error) {
	p.sendBetRegister(messageId, betContent)
	return p.receiveBetRegisterResponse()
}

func (p *Protocol) sendBetRegister(messageId string, betContent BetContent) error {
	packet := Packet{
		Command:   "REGISTER_BET",
		ClientId:  p.clientId,
		MessageId: messageId,
		Content:   betContent.Serialize(),
	}
	return p.sendMessage(packet)
}

func (p *Protocol) sendMessage(packet Packet) error {
	serializedPacket := packet.Serialize()
	messageLength := p.calculatePacketLength(serializedPacket)
	message := fmt.Sprintf("%s%s", string(messageLength), serializedPacket)
	return p.socket.Send([]byte(message))
}

func (p *Protocol) calculatePacketLength(packet string) []byte {
	return network.Htonl(uint32(len(packet)))
}

func (p *Protocol) receiveBetRegisterResponse() (*PacketResponse, error) {
	packetLength, err := p.receivePacketLength()
	if err != nil {
		return nil, err
	}
	return p.receivePacketResponse(packetLength)
}

func (p *Protocol) receivePacketLength() (uint32, error) {
	packetLength := make([]byte, bytesOfPacketLength)
	if err := p.socket.Receive(packetLength); err != nil {
		return 0, err
	}
	return network.Ntohl(packetLength), nil
}

func (p *Protocol) receivePacketResponse(packetLength uint32) (*PacketResponse, error) {
	serializedPacket := make([]byte, packetLength)
	if err := p.socket.Receive(serializedPacket); err != nil {
		return nil, err
	}
	packetResponse := DeserializePacketResponse(string(serializedPacket))
	return packetResponse, nil
}
