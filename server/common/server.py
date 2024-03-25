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
        self.total_recv = 0
        
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



    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            chunk = self.full_read(client_sock)
            print("CHUNK: ",chunk)

            if chunk:
                #if self.get_header(chunk[-1])[1] != 1:
                #    new_chunk = self.full_read(client_sock)
                #    if new_chunk:
                #        chunk += new_chunk
                addr = client_sock.getpeername()
                bets_received = []
            
                for i in chunk:
                    #logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {i}')
                    i = i.rstrip()
                    bet = self.parse_bet(i)
                    if bet:
                        bets_received.append(bet)
                        self.total_recv += 1
                        print("total bets", self.total_recv)
                    else:
                        print("BET INVALIDA")

                self.full_write(client_sock,f"ack {len(bets_received)}")
                store_bets(bets_received)                    
                logging.info(f"action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}")
            else:

                client_sock.close()


        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:            
            #addr = client_sock.getpeername()
            #self.active_clients.pop(addr[0])
            
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
                logging.error("action: write in socket | result: fail | error: sent = 0")
                break

            total_sent += sent
        return total_sent      

    def full_read(self,sock):
        min_header_len = 4 #PONER COMO CONSTANTE (len en bytes)
        message = ""
        
        read = sock.recv(1024)
        print(read)
        if len(read) <= 0:
            logging.error(f"action: read in socket | result: fail | error: {read}")
            return None
        
        if read:
            message += read.decode('utf-8')

            #if first bet read is the last, return
            msg_len, last_msg = self.get_header(message)
            if msg_len == None:
                return None
            if last_msg == 1:
                return message, last_msg
            
            #else, read what arrived
            bets = message.split('$')
            last = bets.pop() #remove last element, which is empty
            #if last bet read is not the last, keep reading
            bet, flag_last = self.get_header(bets[len(bets)-1])
            while flag_last == 0:
                new = sock.recv(1024)
                new_message += new.decode('utf-8')
                if len(new) == 0:
                    logging.error("action: read in socket | result: fail | error: {e}")
                    return None 
                new_bets = new_message.split("$")
                bets += new_bets
                bet, flag_last = self.get_header(new_bets[len(new_bets)-1])

        return bets

    def get_header(self, msg):
        if msg == '':
            return None,None
        header = ""
        for i in range(0,len(msg)-1):
            if msg[i] == "|":
                break
            header += msg[i]

        header_parts = header.split(" ")
        msg_len = header_parts[1]
        last_msg = header_parts[0]
        return msg_len, last_msg

    def parse_bet(self, msg):
        """
        The message received from the client is a string with the following format:
        <header> | <agencia> | <nombre>|<apellido>|<documento>|<nacimiento>|<numero>|$
        0/1 len
            0         1          2          3          4           5           6
        """        
        categorias = msg.split("|")
        categorias.pop() #last is always empty
        if len(categorias) != 7:
            return None
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
        #print data
        bet = Bet(agencia, nombre, apellido, documento, nacimiento, numero)
        return bet
        
