import socket
import logging
import signal
import sys
from common.utils import *
from common.protocol import *

total_clients = 5

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        # { client sockets, id }
        self.client_sockets = {}

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        signal.signal(signal.SIGTERM, self.__handle_SIGTERM)
        clients_served = 0

        # the server
        while clients_served < total_clients:
            client_sock = self.__accept_new_connection()
            self.__handle_client_connection(client_sock)
            clients_served += 1    

        # Process results
        results = self.__process_results()
        logging.info(f"action: raffle | result: success")

        # Send results
        send_results_to_clients(self, results)

        # Finish connections
        for client_sock in self.client_sockets:
            sock_address = client_sock.getpeername()  
            sock_ip = sock_address[0]  
            sock_port = sock_address[1]  
            logging.info(f"action: finish_connection | result: success | remote_address: {sock_ip}:{sock_port}")
            self.__close_socket(client_sock)


    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            while True:
                bets = receive_bets(client_sock)
                if bets == []:
                    break

                store_bets(bets)

                logging.info(f'action: store_bets | result: success | total_bets: {len(bets)}')
                send_confirmation(client_sock)

        except OSError as e:
            logging.error(f"action: client_disconnected | result: fail | error: {e}")
            self.__close_socket(client_sock)

        finally:
            sock_address = client_sock.getpeername()  
            sock_ip = sock_address[0]  
            sock_port = sock_address[1]  
            logging.info(f"action: all_bets_were_sent | result: success | remote_address: {sock_ip}:{sock_port}")


    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        
        # Recieve the id client
        idRaw = c.recv(4)
        if not idRaw:
            raise OSError("Client disconnected")

        id_agency = struct.unpack("!I", idRaw)[0]

        # Add new client socket to the record
        self.client_sockets[c] = id_agency
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]} id: {id_agency}')
        return c

    def __handle_SIGTERM(self, sig, frame):
        logging.info('SIGTERM received, shutting down gracefully')

        self._server_socket.close()

        for client_sock in self.client_sockets:
            client_sock[0].close()

        self.client_sockets.clear()

        sys.exit(0)

    def __process_results(self):
        bets = load_bets()
       
        #{ agency_num, {tot_winners, [winners]} }
        results = {}

        for bet in bets: 
            if has_won(bet):
                agency_number = bet.agency

                # Verify if the agency has any entry
                if agency_number not in results:
                    results[agency_number] = {"total_winners": 0, "winner_documents": []}

                # Add 1 to total_winners
                results[agency_number]["total_winners"] += 1

                # Add document winner
                results[agency_number]["winner_documents"].append(bet.document)

        return results

    def __close_socket(self, client_sock):
        client_sock.close()