import socket

class SocketTCP:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket = None

    def close(self):
        if self._socket:
            try:
                self._socket.shutdown(socket.SHUT_RDWR)
            finally:
                self._socket.close()
                self._socket = None

    def bind_and_listen(self, backlog):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port))
        host, port = self.getsockname()
        self._host = host
        self._port = port
        self._socket.listen(backlog)

    def accept(self):
        connection, address = self._socket.accept()
        host, port = address
        socket = SocketTCP(host, port)
        socket._socket = connection
        return socket, address

    def send(self, data):
        remainingBytes = len(data)
        while remainingBytes > 0:
            sent = self._socket.send(data)
            remainingBytes -= sent
            data = data[sent:]

    def receive(self, size):
        remainingBytes = size 
        receivedData = b""
        while remainingBytes > 0:
            data = self._socket.recv(remainingBytes)
            receivedData += data
            remainingBytes -= len(data)

        return receivedData

    def getsockname(self):
        return self._socket.getsockname()

    def getpeername(self):
        return (self._host, self._port)