import socket
import logging
import signal
from .utils import Bet, store_bets, load_bets, has_won

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.active_clients = {}
        self.running = True
        self.ended = {}
        
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



    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            batch = 8
            bets = []
            message,last = self.full_read(client_sock)
            message = message.rstrip()
            print("FIRST MESSAGE",message)
            if message == "win":
                self.ended[last] = client_sock
                self.get_winners(client_sock, last)
                return
            bet = parse_bet(message)
            if bet:
                bets.append(bet)
            else:
                print("BET INVALIDA")
            
            i = 0
            while message:
                message,last = self.full_read(client_sock)
                if message == "end":
                    self.ended[last] = client_sock
                    break
                if message == "win":
                    self.ended[last] = client_sock
                    self.get_winners(client_sock, last)
                    break
                if message:
                    message = message.rstrip()
                    bet = parse_bet(message)
                    if bet:
                        bets.append(bet)
                    else:
                        print("BET INVALIDA")
                    i += 1
                if i == batch-1:
                    break

            for bet in bets:
                logging.info(f"action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}")
            store_bets(bets)     
            if message != "win":   
                self.full_write(client_sock,f"ack {len(bets)}")


        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            if client_sock not in self.ended.values():
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
        if msg == "win 0\n":
            print("SENDING WINNER SENDING WINNER")
        total_sent = 0
        #header
        msg_len = str(len(msg))
        msg = msg_len + "|" + msg
        print("SENDING: ", msg)
        while total_sent < len(msg):
            sent = sock.send("{}\n".format(msg[total_sent:]).encode('utf-8')) 
            if sent == 0:
                print("SOCKET CERRADO: sent = 0")
                logging.error("action: write in socket | result: fail | error: sent = 0")
                break

            total_sent += sent
        return total_sent      
    
    def get_winners(self,sock, number): #
        print("GET WINNERS")
        if len(self.ended.keys()) == 1:
            logging.info("action: get_winners | result: success")
            bets = load_bets()
            winners = filter(has_won, bets)

            amount_of_winners = {}
            for winner in winners:
                print(winner.agency, winner.number) #cambiar number por dni
                # Corrected logic: Increment wins per agency, not per number
                if winner.agency in amount_of_winners:
                    amount_of_winners[winner.agency] += 1
                else:
                    amount_of_winners[winner.agency] = 1

            print("AMOUNT OF WINNERS",amount_of_winners)
            print("ENDED",self.ended)
            print("WINNERS",winners)
            for client in self.ended.keys():
                client_sock = self.ended[client]
                if client not in amount_of_winners.keys():
                    self.full_write(client_sock, f"win 0\n")
                else:
                    self.full_write(client_sock, f"win {len(amount_of_winners[client])}\n")
                client_sock.close()
            
            logging.info("action: consulta_ganadores | result: success | cant_ganadores: ${CANT}")    



    def full_read(self,sock):
        message = ""
        msg = sock.recv(1)
        if msg == b'':
            return None, None
        
        while msg != b"|":
            message += msg.decode('utf-8')
            msg = sock.recv(1)

        print("read ",message)
        
        if message == "win":
            print("LEYO MENSAJE WIN")
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
        len, last = get_header(message)
        
        message += "|"
        
        payload = sock.recv(int(len)-1)
        if msg == b'':
            return None, None
        message += payload.decode('utf-8')
        print("MENSAJE: ",message)
        
        return message,last

def parse_bet(msg):
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
        
    

def get_header(msg):
    header_parts = msg.split(" ")
    msg_len = header_parts[1]
    last_msg = header_parts[0]
    return msg_len, last_msg
            