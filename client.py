from multiprocessing.connection import Client

model = "vicuna"
server_address = ('localhost', 8088)   

with Client(server_address , authkey=b'im_server') as conn:
    conn.send(model)
    model_state = conn.recv()

print(model_state)

with Client(('localhost' , model_state[model]['port']) , authkey=b'1234') as conn:
    conn.send("vicuna")
    ans = conn.recv()
    print(ans)