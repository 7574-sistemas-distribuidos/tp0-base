from src.results_registry import ResultsRegistry
from src.communication.packet import PacketResponse

class GetWinnersCommand:
    def __init__(self, packet):
        self.packet = packet

    def execute(self):
        result_registry = ResultsRegistry()

        try:
            winners = result_registry.get_winners(self.packet.client_id)
            data =  "\n".join([winner.document for winner in winners])
            if (len(data) > 0):
                data += "\n"
            return PacketResponse(PacketResponse.status_ok, data)
        except Exception as e:
            error_message = str(e)
            return PacketResponse(PacketResponse.status_ko, error_message)
