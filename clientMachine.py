
import numpy as np
from Pyfhel import Pyfhel, PyCtxt,PyPtxt
import tempfile
import os
import struct
import pickle
import selectors
import socket


sendSock = ('127.0.0.1',50001)
recvSock = ('127.0.0.1', 50002)

sel = selectors.DefaultSelector()

tmp_dir = tempfile.TemporaryDirectory()
tmp_dir_name = tmp_dir.name

def clientSocketCreator(info):
    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:  
        sock.connect(info)
        return True,sock
    except ConnectionRefusedError as conn_err:
        return False,sock

def contextCreator(params):
    HE = Pyfhel()
    HE.contextGen(**params)
    HE.keyGen()
    HE.rotateKeyGen()
    HE.relinKeyGen()
    return HE


if __name__ == "__main__": 
    #_,sSock = socketCreator(sendSock)
   # _,rSock = socketCreator(recvSock)

    # Generate Pyfhel session
    print(f"[Client] Initializing Pyfhel session and data...")
    context_params={'scheme':'BFV', 'n':2**13, 't':65537, 't_bits': 20, 'sec':128 }
    HE_Cl =contextCreator(context_params)

    
    # Generate and encrypt data
    x = np.array([1, 2, 3, 4])
    cx = HE_Cl.encodeInt(x)

    y = np.array([5,6,7,8])


    valid_inputs = ["send_he", "send_data", "operations"]

    while True:
        inp = 'send_he' #input(f'enter commands: {*valid_inputs,}').lower()
        if inp not in valid_inputs:
            print("input invalid")
            continue

        verify,sendSock = clientSocketCreator(sendSock)
        if verify == False:
            print("connection refused from method: clientSocketCreator(info)")
            exit()

        if inp == 'send_he':
            HE_ctx =HE_Cl.to_bytes_context()
            print(type(HE_ctx))
            sendSock.send("HE")
            sendSock.sendall(HE_ctx)

        
    


    
    
    













    










