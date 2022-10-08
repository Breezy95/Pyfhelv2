
import numpy as np
from Pyfhel import Pyfhel, PyCtxt,PyPtxt
import tempfile

import os
#import seaborn as sns
import pickle
import selectors
import socket


sendSock = ('127.0.0.1',50001)
recvSock = ('127.0.0.1', 50002)

sel = selectors.DefaultSelector()

tmp_dir = tempfile.TemporaryDirectory()
tmp_dir_name = tmp_dir.name

def socketCreator(info):
    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(info)
    return True,sock




if __name__ == "__main__": 
    #_,sSock = socketCreator(sendSock)
   # _,rSock = socketCreator(recvSock)

    # Generate Pyfhel session
    print(f"[Client] Initializing Pyfhel session and data...")
    HE_client = Pyfhel(context_params={'scheme':'BFV', 'n':2**13, 't':65537, 't_bits': 20, 'sec':128 })
    HE_client.keyGen()             # Generates both a public and a private key
    HE_client.relinKeyGen()
    HE_client.rotateKeyGen()

    # Generate and encrypt data
    x = np.array([1, 2, 3, 4])
    cx = HE_client.encrypt(x)

    y = np.array([5,6,7,8])

    
    
    













    










