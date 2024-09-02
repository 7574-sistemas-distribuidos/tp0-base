import logging
from src.communication.bet_content import BetContent
from src.communication.packet import PacketResponse
from src.utils import Bet, store_bets


class RegisterBetsCommand:
    _new_line_separator = "\n"

    def __init__(self, packet):
        self._packet = packet
        self._valid_bets = []
        self._invalid_bets = []

    def execute(self):
        serialized_bets_content = self._packet.data

        for serialized_bet_content in serialized_bets_content.splitlines():
            self._validate_bet_content(serialized_bet_content)

        store_bets(self._valid_bets)
        if len(self._invalid_bets) > 0:
            logging.info(
                f"action: apuesta_recibida | result: fail | cantidad: ${len(self._invalid_bets)}"
            )
            data = f"{RegisterBetsCommand._new_line_separator.join(self._invalid_bets)}{RegisterBetsCommand._new_line_separator}"
            return PacketResponse(PacketResponse.status_ko, data)
        else:
            logging.info(
                f"action: apuesta_recibida | result: success | cantidad: ${len(self._valid_bets)}"
            )
            return PacketResponse(PacketResponse.status_ok, "")

    def _validate_bet_content(self, serialized_bet_content):
        try:
            bet_content = BetContent.deserialize(serialized_bet_content)
            bet = Bet(
                self._packet.client_id,
                bet_content.name,
                bet_content.lastname,
                bet_content.id_number,
                bet_content.birthdate,
                bet_content.bet_number,
            )
            self._valid_bets.append(bet)
        except Exception as e:
            self._invalid_bets.append(serialized_bet_content)
