import socket
import logging
import signal
import sys
import threading
from common.utils import *
from common.protocol import *

total_clients = 5

# Define a locks
store_bets_lock = threading.Lock()

def thread_safe_store_bets(bets):
    with store_bets_lock:
        store_bets(bets)

load_bets_lock = threading.Lock()

def thread_safe_load_bets():
    with load_bets_lock:
        return load_bets()


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        # { client sockets, id }
        self.client_sockets = {}
        self.client_threads = []

        # Event to sincronize
        self.all_bets_were_sent_event = threading.Event()

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
            client_sock, id_agency = self.__accept_new_connection()
            client_thread = threading.Thread(target=self.__handle_client_connection, args=(client_sock, id_agency))
            client_thread.start()
            self.client_threads.append(client_thread)
            clients_served += 1    

        # Wait for all client threads to finish
        for client_thread in self.client_threads:
            client_thread.join()


    def __handle_client_connection(self, client_sock, id_agency):
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

                thread_safe_store_bets(bets)  # Usar la función envoltorio thread_safe_store_bets

                logging.info(f'action: store_bets | result: success | total_bets: {len(bets)}')
                send_confirmation(client_sock)

            logging.info(f"action: all_bets_were_sent | result: success | id_agency: {id_agency}")

            self.all_bets_were_sent_event.set()
            self.all_bets_were_sent_event.wait()
            
            bets = thread_safe_load_bets()

            filtered_bets = [bet for bet in bets if bet.agency == id_agency]

            # Process results
            results = self.__process_results(filtered_bets)
            logging.info(f"action: raffle | result: success")

            # Send results
            send_results_to_clients(self, client_sock, results, id_agency)

        except OSError as e:
            logging.error(f"action: client_disconnected | result: fail | error: {e}")
            self.__close_socket(client_sock)

        finally: 
            logging.info(f"action: finish_connection | result: success | id_agency: {id_agency}")
            self.__close_socket(client_sock)


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
        return c, id_agency

    def __handle_SIGTERM(self, sig, frame):
        logging.info('SIGTERM received, shutting down gracefully')

        self._server_socket.close()

        for client_sock in self.client_sockets:
            client_sock[0].close()

        self.client_sockets.clear()

        sys.exit(0)

    def __process_results(self, bets):
        total_winners = 0
        winner_documents = []

        for bet in bets: 
            if has_won(bet):
                # Add 1 to total_winners
                total_winners += 1

                # Add document winner
                winner_documents.append(bet.document)

        results = {"total_winners": total_winners, "winners": winner_documents}

        return results

    def __close_socket(self, client_sock):
        client_sock.close()