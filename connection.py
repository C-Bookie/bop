
import socket
import threading
import json
import struct

class Connection(threading.Thread):
    def __init__(self, conn):
        super(Connection, self).__init__()
        self.conn = conn
        self.listeners = {}

        self.daemon = True
        self.start()

    def setListener(self, com, fun):
        self.listeners[com] = fun

    def run(self):
        while True:
            try:
                self.data = self.recv_msg().decode()
                if self.data != "":

                    rec = json.loads(self.data)

                    if rec["com"] in self.listeners:
                        self.listeners[rec["com"]](rec)

            except socket.error as e:
                #if e.errno == errno.ECONNRESET:
                self.conn.close()
                break
            except Exception as e:
                raise (e)

    def send_msg(self, msg):
        try:
            msg = struct.pack('>I', len(msg)) + msg
            self.conn.sendall(msg)
        except socket.error as e:
            print("error")
            #                if e.errno == errno.ECONNRESET:
            global loop
            loop = False
            self.conn.close()

    def send_set(self, s):
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            else:
                return obj.list()

        data = json.dumps(s, default=set_default)
        self.send_msg(data.encode())

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


