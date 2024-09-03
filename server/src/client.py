from src.communication.command_dispatcher import CommandDispatcher
from src.communication.protocol import Protocol
from threading import Thread
import logging

class Client:
    def __init__(self, socket):
        self._thread = None
        self._socket = socket
        self._is_running = True

    def start(self):
        self._thread = Thread(target=self._run)
        self._thread.start()

    def _run(self):
        try:
            protocol = Protocol(self._socket)
            command = ""
            while command != "CLOSE_LOAD_OF_BETS" and command != "GET_WINNERS":
                packet = protocol.receivePacket()
                command = packet.command
                packetResponse = CommandDispatcher.dispatch(packet)
                protocol.sendPacket(packetResponse)                    
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            self._is_running = False

    def join(self):
        self._thread.join()
        self._socket.close()

    def stop(self):
        self._is_running = False
        self._socket.close()

    def is_running(self):
        return self._is_running