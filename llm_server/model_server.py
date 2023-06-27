from concurrent import futures
import random
import grpc
from multiprocessing.connection import Listener , wait , Client
import threading
import time
import subprocess
import queue
from model_server_pb2 import  modelRequest , modelResponse , modelName , modelInfo , empty
import model_server_pb2_grpc
import utils.LLM_model_service as LLM

    

# expire_time = 5
def load_config():
    model_state =   {
                    "vicuna" : 
                    {
                        "state" : 0 , 
                        "port" : 9001,
                        "last_used" : 0,
                        "token" : 0
                    },
                }

    user_record = {"vicuna" : {}}

    current_user = {}
    expire_time = 35 * 60

    return model_state , user_record , expire_time  , current_user


def serve():

    
    global thread_state
    thread_state = True
    model_state , user_record , expire_time , current_user = load_config()



    model_queue = {i:queue.Queue() for i in model_state.keys()}
    t = threading.Thread(target= LLM.communicate_queue , args= (model_queue['vicuna'], model_state , "vicuna" , current_user , thread_state))
    t.start()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_server_pb2_grpc.add_LLMServiceServicer_to_server(LLM.LLM_model_service(model_state , model_queue , user_record , current_user), server)
    print('server start ')
    server.add_insecure_port("[::]:50051")
    server.start()

    # check model is idel
    while True:
        time.sleep(30)
        print(model_state)
        for model_name , model_info in model_state.items():
            now = time.perf_counter()
            print(now - model_info['last_used'])
            if now - model_info['last_used']  > expire_time:
                user_record = LLM.delete_model_proc(model_state , model_name)


    

if __name__ == '__main__':
    
    serve()
    

    # check_loop()