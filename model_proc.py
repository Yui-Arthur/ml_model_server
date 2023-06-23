from multiprocessing.connection import Listener
from model_server_pb2 import ( modelRequest , modelResponse )

address = ('localhost', 9001)   

with Listener(address, authkey=b'1234') as listener:
    
    while True:
        conn = listener.accept()
        command = conn.recv()

        if command == 'del':
            conn.send("ok")
            break
        
        conn.send(modelResponse(prompt = "yes" , response = "no"))
        conn.close()
        # print('connection accepted from', listener.last_accepted)

        #  conn.recv()