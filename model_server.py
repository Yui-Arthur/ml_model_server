from concurrent import futures
import random
import grpc
from model_server_pb2 import  modelRequest , modelResponse
import model_server_pb2_grpc
from multiprocessing.connection import Listener , wait , Client
import threading
import time
import subprocess


def create_model_proc(model_name):
    model_state[model_name]['last_used'] = time.perf_counter()
    model_state[model_name]['state'] = 1
    subprocess.Popen(["python", "model_proc.py" , model_name])

def delete_model_proc(model_name):
    try:
        conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
        conn.send('del')
        print(conn.recv())
        conn.close()
    except:
        model_state[model_name]['state'] = 0


def communicate_model(model_name , user , prompt):
    conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
    conn.send((user , prompt))
    response = conn.recv()
    conn.close()
    return response


class send_to_model(model_server_pb2_grpc.sendToModelServicer):
    def getModelResponse(self , request , context):
        
        model_name = request.modelName
        user = request.user
        prompt = request.prompt

        if model_name not in model_state:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found")

        if model_state[model_name]['state'] == 0:
            create_model_proc(model_name) 
            context.abort(grpc.StatusCode.NOT_FOUND, "Model is loadding , try again")
        else:
            model_state[model_name]['last_used'] = time.perf_counter()
            response = communicate_model(model_name , user , prompt)
            return response
        # return  modelResponse(prompt = "1234" , response = "3467")
    
model_state =   {
                    "vicuna" : 
                    {
                        "state" : 0 , 
                        "port" : 9001,
                        "last_used" : 0
                    },
                }

expire_time = 35 * 60
# expire_time = 5


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_server_pb2_grpc.add_sendToModelServicer_to_server(send_to_model(), server)
    print('server start ')
    server.add_insecure_port("[::]:50051")
    server.start()
    # server.wait_for_termination()
    while True:
        time.sleep(5)
        print(model_state)
        for model_name , model_info in model_state.items():
            now = time.perf_counter()
            print(now - model_info['last_used'])
            if now - model_info['last_used']  > expire_time:
                delete_model_proc(model_name)

def check_loop():
    pass

if __name__ == '__main__':
    serve()
    # check_loop()