from src.results_registry import ResultsRegistry
from src.communication.packet import PacketResponse

class CloseLoadOfBetsCommand:
    def __init__(self, packet):
        self.packet = packet

    def execute(self):
        result_registry = ResultsRegistry()
        result_registry.close_agency(self.packet.client_id)
        return PacketResponse(PacketResponse.status_ok, "")