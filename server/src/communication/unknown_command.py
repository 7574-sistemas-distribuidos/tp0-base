import logging
from src.communication.packet import PacketResponse

class UnknownCommand:
    def __init__(self, packet):
        self.packet = packet
    
    def execute(self):
        packetResponse = PacketResponse(PacketResponse.status_ko)
        logging.debug(f"action: receive_message | result: fail | error: unknown command")
        return packetResponse
