import socket
import logging
import signal
from .utils import Bet, store_bets

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.active_clients = {}
        self.running = True
        self.bets = []
        
    def handle_sigterm(self):
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

        store_bets(self.bets) 

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            read = self.full_read(client_sock)
            if read:
                msg = read.rstrip().decode('utf-8')
                addr = client_sock.getpeername()
                messages = msg.split("$")

                messages.pop()
                size_of_batch = int(read[0]) # read.count($)
                for i in range(0,len(messages)):
                    bet = self.parse_bet(messages[i])
                    self.bets.append(bet)    
                
                #if len(bets) == size_of_batch:
                self.full_write(client_sock,f"ack {size_of_batch}")
                
                logging.info(f"action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}")


                #else:
                #    self.full_write(client_sock,f"err {len(bets)}")

                logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg}')
            



        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:           
            addr = client_sock.getpeername()
            self.active_clients.pop(addr[0])
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
                logging.error("SOCKET CERRADO")
                return None

    def full_write(self,sock, msg):
        total_sent = 0
        #header
        msg_len = str(len(msg))
        msg = msg_len + "|" + msg

        while total_sent < len(msg):
            sent = sock.send("{}\n".format(msg[total_sent:]).encode('utf-8')) 
            if sent == 0:
                print("SOCKET CERRADO: sent = 0")
                logging.error("action: write in socket | result: fail | error: {e}")
                break

            total_sent += sent
        return total_sent      

    def full_read(self,sock):
        header_len = 1 #PONER COMO CONSTANTE (len en bytes)
        bytes_read = b''
        read = sock.recv(1024)
        if len(read) <= 0:
            logging.error("action: read in socket | result: fail | error: {e}")
            return None

        if read and len(read) > 2:
            msg_len = int(read[:header_len].decode('utf-8'))
            bytes_read += read

            remaining = msg_len - len(bytes_read)

            while len(bytes_read) < int(msg_len):
                read = sock.recv(remaining)
                bytes_read += read
                remaining = msg_len - len(bytes_read)
                if len(read) <= 0: #codigo repetido
                    logging.error("action: read in socket | result: fail | error: {e}")
                    return None 
                
        return bytes_read

    def parse_bet(self, msg):
        """
        The message received from the client is a string with the following format:
        <len> | <agencia> | <nombre>|<apellido>|<documento>|<nacimiento>|<numero>
          0         1          2          3          4           5          6
        """        
    
        categorias = msg.split("|")
        for i in range(1,len(categorias)):
            categoria = categorias[i].split(" ")
            categoria.pop(0)
            categorias[i] = " ".join(categoria)

        agencia = categorias[1]
        nombre = categorias[2]
        apellido = categorias[3]
        documento = categorias[4]
        nacimiento = categorias[5]
        numero = categorias[6]

        bet = Bet(agencia, nombre, apellido, documento, nacimiento, numero)
        return bet
        
