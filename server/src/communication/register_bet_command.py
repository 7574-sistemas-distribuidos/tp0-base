import logging
from src.communication.bet_content import BetContent
from src.communication.packet import PacketResponse
from src.utils import Bet, store_bets


class RegisterBetCommand:
    def __init__(self, packet):
        self.packet = packet

    def execute(self):
        serializedBetContent = self.packet.data
        betContent = BetContent.deserialize(serializedBetContent)
        
        client_id = self.packet.client_id
        bet = Bet(client_id, betContent.name, betContent.lastname, betContent.id_number, betContent.birthdate,
            betContent.bet_number)
        store_bets([bet])
        logging.info(f"action: apuesta_almacenada | result: success | dni: ${bet.document} | numero: ${bet.number}")

        packetResponse = PacketResponse(PacketResponse.status_ok)
        return packetResponse
