from multiprocessing.connection import Listener , wait , Client
import threading
import time
import subprocess

address = ('localhost', 8088)   
model_state =   {
                    "vicuna" : 
                    {
                        "state" : 0 , 
                        "port" : 9001,
                        "last_used" : 0
                    },
                }

expire_time = 35 * 60
expire_time = 5

def listener():
    with Listener(address, authkey=b'im_server') as listener:
        while True:
            conn = listener.accept()

            model_name = conn.recv()
            conn.send(model_state)
            conn.close()

            if model_state[model_name]['state'] == 0:
                create_model_proc(model_name)
            else:
                model_state[model_name]['last_used'] = time.perf_counter()
            # print('connection accepted from', listener.last_accepted)


def delete_model_proc(model_name):
    try:
        conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
        conn.send('del')
        print(conn.recv())
        conn.close()
    except:
        model_state[model_name]['state'] = 0

def create_model_proc(model_name):
    model_state[model_name]['last_used'] = time.perf_counter()
    model_state[model_name]['state'] = 1
    subprocess.Popen(["python", "model.py" , model_name])

t = threading.Thread(target = listener)  
t.start()
# print(model_state)
# create_model_proc("vicuna")
    
while True:
    time.sleep(5)
    print(model_state)
    for model_name , model_info in model_state.items():
        now = time.perf_counter()
        print(now - model_info['last_used'])
        if now - model_info['last_used']  > expire_time:
            delete_model_proc(model_name)


