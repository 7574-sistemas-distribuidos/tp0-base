import multiprocessing as mp

class Abstract_client:
    def __init__(self,socket,client_id):
        self.clients = {}
        self.client_id = 0
        self.parent_conn, self.child_conn = mp.Pipe()
        self.sock = socket
        return self.parent_conn

        def send_to_client(self, message):
            pass

        def receive_from_client(self):
            pass



