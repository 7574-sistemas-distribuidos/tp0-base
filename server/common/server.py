import socket
import logging
import signal
from .utils import store_bets, load_bets, has_won
from abstract_client import Abstract_client

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.active_clients = {}
        self.running = True
        self.ended = 0
        self.ready = {}
        
    def handle_sigterm(self, signum, frame):
        logging.info("HANDLING SIGTERM")
        self.running = False
        for client in self.active_clients.values():
            client.close()
        self._server_socket.close()

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """
        signal.signal(signal.SIGTERM, self.handle_sigterm)

        while self.running:
            client_sock = self.__accept_new_connection()
            if client_sock:
                self.__handle_client_connection(client_sock)
        self._server_socket.close()


    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            message,last = self.full_read(client_sock)
            #while message and self.running: 
            #idea: esto podria ser un match
            match message:  
                case "win":
                    self.get_winners(client_sock, last)
                case "end":
                    self.ended +=1
                case "bet":
                    bet = parse_bet(message)
                    store_bets(bet)
                    logging.info(f"action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}")

            if message != "win": 
                self.full_write(client_sock,f"ack {len(bets)}")

        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            if client_sock not in self.ready.values():
                client_sock.close()


    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """
        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        if self.running:
            try:
                c, addr = self._server_socket.accept()
                logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
                self.active_clients[addr[0]] = c
                return c
            except:
                return None
    
    def get_winners(self,sock,last): #
        self.ready[last] = sock
        if self.ended < 5:
            return
        
        logging.info("action: get_winners | result: success")
        bets = load_bets()
        winners = filter(has_won, bets)
        amount_of_winners = {}
        for winner in winners: 
            if str(winner.agency) in amount_of_winners:
                amount_of_winners[str(winner.agency)].append(winner.document) 
            else:
                amount_of_winners[str(winner.agency)] = []
                amount_of_winners[str(winner.agency)].append(winner.document)
        
        for client in self.ready.keys():
            client_sock = self.ready[client]
            message = "win" 
            if client in amount_of_winners.keys():
                client_winners = amount_of_winners[client]
                message += f" {len(client_winners)} "
                for i in client_winners:
                    message += " " + i
            else:
                message += " 0"
            message += "\n"
            self.full_write(client_sock, message)
    
        self.running = False  # Stop the server loop


    def full_read(self,sock):
        #saque partes y las puse en abstract_client
        #esto deberia estar en analisis de mensaje
        if message == "win":
            client_id = ""
            for _ in range(1):
                msg = sock.recv(1)
                client_id += msg.decode('utf-8')
            self.get_winners(sock, client_id)
            return "win", client_id
        
        if message == "end":
            msg = sock.recv(1)
            last = msg.decode('utf-8')
            return "end", last
        
        return message,last
    

            