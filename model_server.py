from concurrent import futures
import random
import grpc
from model_server_pb2 import  modelRequest , modelResponse , modelName , modelInfo , empty
import model_server_pb2_grpc
from multiprocessing.connection import Listener , wait , Client
import threading
import time
import subprocess
import queue

def create_model_proc(model_name , max_token = 150):
    model_state[model_name]['last_used'] = time.perf_counter()
    model_state[model_name]['state'] = 1
    subprocess.Popen(["python", "model_proc.py" , "--max-tokens", str(max_token)])

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

def communicate_queue(single_model_queue , model_name):
    while True:
        if not single_model_queue.empty():
            user_request_dic = single_model_queue.get()
            print(user_request_dic)
            res = communicate_model(model_name , user_request_dic['user'] , user_request_dic['prompt'])
            user_request_dic['response'] = res
            user_request_dic['end_time'] = time.perf_counter()


class send_to_model(model_server_pb2_grpc.sendToModelServicer):
    def getModelResponse(self , request , context):
        
        model_name = request.modelName
        user = request.user
        prompt = request.prompt

        

        if model_name not in model_state:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found")

        if model_state[model_name]['state'] == 0:
            create_model_proc(model_name , 150) 
            time.sleep(60)
        

        model_state[model_name]['last_used'] = time.perf_counter()
        request_dic = {'name': model_name,'user':user,'prompt': prompt ,'response':None, 'start_time':time.perf_counter() , 'end_time' : 0}

        model_queue[model_name].put(request_dic)

        while request_dic['response'] == None : pass

        print(request_dic['response'])

        return request_dic['response']
    
    def deleteModelProc(self, request , context):
        model_name = request.modelName

        if model_name not in model_state or model_state[model_name]['state'] == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found or not running")

        delete_model_proc(model_name)
        return modelInfo(modelInfo = str(model_state[model_name]))
    
    def checkModelState(self, request , context):
        model_name = request.modelName

        if model_name not in model_state:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found")

        return modelInfo(modelInfo = str(model_state[model_name]))
    
    def createModelProc(self, request , context):
        model_name = request.modelName
        max_token = request.maxToken
        
        if model_name not in model_state:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found")

        print(model_name , max_token)        
        create_model_proc(model_name) 

        return modelInfo(modelInfo = str(model_state[model_name]))
    
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


def model_queue_thread():
    global model_queue 
    model_queue = {i:queue.Queue() for i in model_state.keys()}
    t = threading.Thread(target= communicate_queue , args= (model_queue['vicuna'], "vicuna",))
    t.start()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_server_pb2_grpc.add_sendToModelServicer_to_server(send_to_model(), server)
    print('server start ')
    server.add_insecure_port("[::]:50051")
    server.start()

    # check model is idel
    while True:
        time.sleep(15)
        print(model_state)
        for model_name , model_info in model_state.items():
            now = time.perf_counter()
            print(now - model_info['last_used'])
            if now - model_info['last_used']  > expire_time:
                delete_model_proc(model_name)


if __name__ == '__main__':
    model_queue_thread()
    serve()
    # check_loop()