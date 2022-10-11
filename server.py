import pickle
import threading
import logging
from math import remainder
import tempfile
import socket
import socketserver
import struct
import types
from Pyfhel import Pyfhel,PyCtxt,PyPtxt



recvaddr = ('localhost',50001)
sendaddr = ('localhost',50002)

#called when socket is done receiving data,
# or when client closes connection
def accept_wrapper(sock):
    conn,addr = sock.accept()

def socketCreator(info):
    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    success =sock.connect_ex(info)
    if success == 0:
        return True,sock
    else:
        return False,sock

def serverSocket(info):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(recvaddr)
    sock.listen()
    conn,addr = sock.accept()
    return conn,addr

def contextCreator(params):
    HE = Pyfhel()
    HE.contextGen(**params)
    HE.rotateKeyGen()
    HE.relinKeyGen()
    return HE



'''1st 4 bits of pickled message are data size, next 4 are for the operation, rest is '''
def recvMessage(conn):
    try:
        msg = conn.recv(4)
        pload_size = struct.unpack('>I',msg)[0]
        operation = struct.unpack('>I',msg)[0]
        pick_payload = bytes()
        remainder_size= pload_size
        while remainder_size >0:
            pick_payload = pick_payload + conn.recv(remainder_size)
            remainder_size -= len(pick_payload)
        unpick_payload = pickle.loads(pick_payload)
        return operation,unpick_payload


    except:
        pass


class TCPHandler(socketserver.BaseRequestHandler):

    def __init__(self,request ,clientAddress, server):
        self.logger = logging.getLogger("TCPHandler")
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self,request, clientAddress,server)
        return
    
    def setup(self):
        self.logger.debug('TCPHandler, setup method')
        return socketserver.BaseRequestHandler.setup(self)
    
    def handle(self):
        self.logger.debug('TCPHandler, handle method')
        msg =self.request.recv(8)
        self.request.send(b'12345')
        #1st 8 bits of message
        #1st 4 are for msg 
        #2nd 4 are for operation

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)


class AppServer(socketserver.TCPServer):
    def __init__(self, server_addr, handler_class=TCPHandler):
        self.logger = logging.getLogger("APPServer")
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_addr,handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(self, request_address)

        socketserver.TCPServer.socket.bind

if __name__ =="__main__":
    
    with AppServer(recvaddr, TCPHandler) as server:
        t = threading.Thread(target=server.serve_forever)
        t.daemon = True
        t.start()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(recvaddr)
        msg = b'hi'
        len_sent =s.send(msg)
        print(f"client: len of msg {len_sent}")
        resp = s.recv(len_sent)
        print(resp)

    

    
    '''
    HE_Server = Pyfhel()
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as recvSock :
        recvSock.bind(recvaddr)
        recvSock.listen()
        print(f"Listening on {recvaddr}")
        recvSock.setblocking(False)
        sel.register(recvSock,selectors.EVENT_READ,data=None)

        while True:
            events = sel.select(timeout=None)
            for key,mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
'''


