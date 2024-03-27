import struct
import logging
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

def receive_bets(socket):
    
    # First 4 bytes indicate number of bets to be received
    num_bets_data = socket.recv(4)
    if not num_bets_data:
        raise OSError("Client disconnected")

    num_bets = struct.unpack("!I", num_bets_data)[0]

    bets = []

    # Client has no more bets to send
    if num_bets == 0:
        return bets

    for _ in range(num_bets):
        bet = receive_bet(socket)
        bets.append(bet)

    return bets    

# Send 1 as a confirmation
def send_confirmation(socket):
    socket.sendall(struct.pack('!i', 1))
    

def send_results_to_clients(self, results):
    
    for client_sock, client_id in self.client_sockets.items():

        # Check if there are results for this client
        if client_id in results:
            result = results[client_id]
            total_winners = result["total_winners"]
            winner_documents = result["winner_documents"]
        else:
            # If no results for this client, set total winners to 0
            total_winners = 0
            winner_documents = []
        
        # Serialize total winners
        total_winners_bytes = struct.pack('!I', total_winners)

        # Serialize documents winners
        documents_bytes = b""
        for document in winner_documents:
            documents_bytes += struct.pack('!I', int(document))

        data_to_send = total_winners_bytes + documents_bytes
        
        # Send results
        try:
            client_sock.sendall(data_to_send)
            logging.info(f"Sent results to client {client_id}")
        except Exception as e:
            logging.error(f"Error sending results to client {client_id}: {e}")