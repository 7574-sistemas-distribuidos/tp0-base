import logging
from src.network.utils import htonl, ntohl
from src.communication.packet import Packet
from src.communication.packet import PacketResponse


class Protocol:
    _bytes_of_packet_length = 4
    _encoding_format = "utf-8"

    def __init__(self, socket):
        self._socket = socket

    def receivePacket(self):
        packetLength = self._receivePacketLength()
        serializedPacket = self._receivePacket(packetLength)
        addr = self._socket.getpeername()
        logging.info(f"action: receive_message | result: success | ip: {addr[0]} | msg: \n{serializedPacket}")
        return Packet.deserialize(serializedPacket)

    def _receivePacketLength(self):
        return ntohl(self._socket.receive(Protocol._bytes_of_packet_length))
    
    def _receivePacket(self, packetLength):
        return self._socket.receive(packetLength).decode(Protocol._encoding_format)

    def sendPacket(self, packet):
        serializedPacket = PacketResponse.serialize(packet)
        packetResponseLength = Protocol._calculatePacketLength(serializedPacket)
        self._sendPacket(packetResponseLength, serializedPacket)

    def _calculatePacketLength(serializedPacket):
        return htonl(len(serializedPacket))

    def _sendPacket(self, length, serializedPacket):
        packet = length + serializedPacket.encode(Protocol._encoding_format)
        self._socket.send(packet)
    