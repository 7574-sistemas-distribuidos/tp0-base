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

func (p *Protocol) RegisterBets(messageId string, betsContent []BetContent) (*PacketResponse, error) {
	p.sendBetsRegister(messageId, betsContent)
	return p.receiveBetRegisterResponse()
}

func (p *Protocol) sendBetsRegister(messageId string, betsContent []BetContent) error {
	content := ""
	for _, betContent := range betsContent {
		content += fmt.Sprintf("%s\n", betContent.Serialize())
	}

	packet := Packet{
		Command:   "REGISTER_BETS",
		ClientId:  p.clientId,
		MessageId: messageId,
		Content:   content,
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

func (p *Protocol) CloseLoadOfBets(messageId string) (*PacketResponse, error) {
	p.sendCloseLoadOfBets(messageId)
	return p.receiveCloseLoadOfBetsResponse()
}

func (p *Protocol) sendCloseLoadOfBets(messageId string) error {
	packet := Packet{
		Command:   "CLOSE_LOAD_OF_BETS",
		ClientId:  p.clientId,
		MessageId: messageId,
	}
	return p.sendMessage(packet)
}

func (p *Protocol) receiveCloseLoadOfBetsResponse() (*PacketResponse, error) {
	packetLength, err := p.receivePacketLength()
	if err != nil {
		return nil, err
	}
	return p.receivePacketResponse(packetLength)
}

func (p *Protocol) GetWinners() (*PacketResponse, error) {
	p.sendGetWinners()
	return p.receiveGetWinnersResponse()
}

func (p *Protocol) sendGetWinners() error {
	packet := Packet{
		Command:  "GET_WINNERS",
		ClientId: p.clientId,
	}
	return p.sendMessage(packet)
}

func (p *Protocol) receiveGetWinnersResponse() (*PacketResponse, error) {
	packetLength, err := p.receivePacketLength()
	if err != nil {
		return nil, err
	}
	return p.receivePacketResponse(packetLength)
}
