import socket
import logging
import signal

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.active_clients = {}
        self.running = True
        
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
            msg = self.full_read(client_sock).rstrip().decode('utf-8')
            addr = client_sock.getpeername()
            logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg}')
            
            if msg:
                self.full_write(client_sock,msg)


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
        #por default escribe un char mas, y sumando el \n, se terminan escribiendo 2 char mas.
        #luego, se leen 2 char de mas en el cliente
        total_sent = 0

        while total_sent < len(msg):
            sent = sock.send("{}\n".format(msg[total_sent:]).encode('utf-8')) 
                #client_sock.send("{}\n".format(msg).encode('utf-8'))
            if sent == 0:
                print("SOCKET CERRADO: sent = 0")
                logging.error("action: write in socket | result: fail | error: {e}")
                break

            total_sent += sent
        return total_sent      

    def full_read(self,sock):
        bytes_read = b''
        while bytes_read[-1:] != b'\n':
            read = sock.recv(1024)
            if len(read) <= 0:
                logging.error("action: read in socket | result: fail | error: {e}")
                return None

            bytes_read += read
        return bytes_read
