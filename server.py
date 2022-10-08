import sys
import socket
import selectors
import types
from Pyfhel import Pyfhel,PyCtxt,PyPtxt

sel = selectors.DefaultSelector()

recvaddr = ('localhost',50001)
sendaddr = ('localhost',50002)

#called when socket is done receiving data,
# or when client closes connection
def accept_wrapper(sock):
    conn,addr = sock.accept()

def socketCreator(info):
    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(info)
    return True,sock

def contextcrafter(params):
    HE = Pyfhel()
    HE.contextGen(**params)
    HE.rotateKeyGen()
    HE.relinKeyGen()
    return HE

if __name__ =="__main__":
    while True:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(recvaddr)
        sock.listen()
        conn,addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(b'HI')
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


