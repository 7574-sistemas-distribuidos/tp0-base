import multiprocessing as mp
import logging
from .utils import Bet


class Abstract_client:
    def __init__(self,socket,client_id):
        self.process = mp.Process(target=self.run, args=(self.child_conn,self.socket))
        self.client_id = 0
        self.parent_conn, self.child_conn = mp.Pipe()
        self.sock = socket

        def run(self, conn,socket):
            pass

        def get_client_id(self):
            return self.client_id

        def full_write(self, msg):
            total_sent = 0
            msg_len = str(len(msg))
            msg = msg_len + "|" + msg
            while total_sent < len(msg):
                sent = self.sock.send("{}\n".format(msg[total_sent:]).encode('utf-8')) 
                if sent == 0:
                    print("SOCKET CERRADO: sent = 0")
                    logging.error("action: write in socket | result: fail | error: sent = 0")
                    break

                total_sent += sent
            return total_sent

        def receive_from_client(self):
            message = ""
            msg = self.sock.recv(1)
            if msg == b'':
                return None
            while msg != b"|":
                message += msg.decode('utf-8')
                msg = self.sock.recv(1)


            len, last = get_header(message)
            message += "|"
            
            payload = self.sock.recv(int(len)-1)
            if msg == b'':
                return None, None
            message += payload.decode('utf-8')
            return message
        
        def get_header(message):
            header = message.split("|")
            return header[0], header[1] #len,last

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


