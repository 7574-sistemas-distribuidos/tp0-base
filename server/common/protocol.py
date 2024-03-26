import struct
from common.utils import Bet

"""
Protocol functions
"""
def receive_data(socket):
    #  |- Id -|------ Name ------|------ LastName ------|- Document -|-- Birthdate  --|- Number -|
    #  |- 4b -|------  24b ------|------   24b    ------|-    4b    -|--    10b     --|-   4b   -|
    total_size = 70  

    # Recibir el mensaje completo
    data = b""
    while len(data) < total_size:
        packet = socket.recv(total_size - len(data))
        if not packet:
            raise OSError("Client disconnected")
        data += packet

    return data

def receive_bet(socket):
    # Receive raw data
    data = receive_data(socket)

    # Unpack data
    agency = struct.unpack("!I", data[:4])[0]
    first_name = data[4:28].decode('utf-8').strip('\x00')
    last_name = data[28:52].decode('utf-8').strip('\x00')
    document = struct.unpack("!I", data[52:56])[0]
    birthdate = data[56:66].decode('utf-8').strip('\x00')  
    number = struct.unpack("!I", data[66:70])[0]

    bet = Bet(agency, first_name, last_name, document, birthdate, number)

    return bet

def send_ack(socket):
    # Send ACK
    socket.send("ACK".encode('utf-8'))