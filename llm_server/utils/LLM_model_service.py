from model_server_pb2 import  modelRequest , modelResponse , modelName , modelInfo , empty , userRecord , queueSize , currentUser
import model_server_pb2_grpc
import time
import grpc
from multiprocessing.connection import Listener , wait , Client
import threading
import time
import subprocess

class LLM_model_service(model_server_pb2_grpc.LLMService):

    def __init__(self , model_state , model_queue , user_record , current_user):
        self.model_state = model_state
        self.model_queue = model_queue
        self.user_record = user_record
        self.current_user = current_user

    def getModelResponse(self , request , context):
        
        model_name = request.modelName
        user = request.user
        prompt = request.prompt

        

        if model_name not in self.model_state:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found")

        if self.model_state[model_name]['state'] == 0:
            create_model_proc(self.model_state , model_name , 150 , self.user_record) 
            # time.sleep(60)
        

        self.model_state[model_name]['last_used'] = time.perf_counter()
        request_dic = {'name': model_name,'user':user,'prompt': prompt ,'response':None, 'start_time':time.perf_counter()}

        self.model_queue[model_name].put(request_dic)

        while request_dic['response'] == None : pass

        print(request_dic['response'])

        return request_dic['response']
    
    def deleteModelProc(self, request , context):
        model_name = request.modelName

        if model_name not in self.model_state or self.model_state[model_name]['state'] == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found or not running")

        self.user_record = delete_model_proc(self.model_state , model_name)
        return modelInfo(modelInfo = str(self.model_state[model_name]))
    
    def checkModelState(self, request , context):

        return modelInfo(modelInfo = str(self.model_state))
    
    def createModelProc(self, request , context):
        model_name = request.modelName
        max_token = request.maxToken
        load_record = request.loadUserRecord
        
        if model_name not in self.model_state or  self.model_state[model_name]['state'] == 2:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found or model is already running")

        print(model_name , max_token , self.user_record)        
        
        if load_record:
            create_model_proc(self.model_state , model_name , max_token , self.user_record) 
        else:
            create_model_proc(self.model_state , model_name , max_token) 

        return modelInfo(modelInfo = str(self.model_state[model_name]))
    
    def checkUSerRecord(self, request , context):
        model_name = request.modelName

        if model_name not in self.model_state or self.model_state[model_name]['state'] == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found or model is not running")
        print(model_name)
        user_record = export_user_record(self.model_state , model_name)
        return userRecord(userRecord=str(user_record))
    
    def showQueurSize(self, request , context):
        model_name = request.modelName

        if model_name not in self.model_state or self.model_state[model_name]['state'] == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found or model is not running")

        # print()
        return queueSize(queueSize=str(self.model_queue[model_name].qsize()))
    
    def showCurrentUser(self, request , context):
        model_name = request.modelName
        if model_name not in self.model_state or self.model_state[model_name]['state'] == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "Model not found or model is not running")

        return currentUser(currentUser=str(self.current_user[model_name]))
    
def create_model_proc(model_state , model_name , max_token = 150 , user_record = {}):
    subprocess.Popen(["python", "model_proc.py" , "--max-tokens", str(max_token)])
    model_state[model_name]['last_used'] = time.perf_counter()
    model_state[model_name]['state'] = 1
    model_state[model_name]['token'] = max_token

    if  test_model_proc(model_state , model_name):
        model_state[model_name]['state'] = 2
        import_user_record(model_state , model_name  , user_record)
    else:
        model_state[model_name]['state'] = 0
        model_state[model_name]['token'] = 0

    
    

def delete_model_proc(model_state , model_name):
    try:
        conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
        conn.send(('del' , 'del'))
        usr_record = conn.recv()
        conn.close()
        model_state[model_name]['state'] = 0
        model_state[model_name]['token'] = 0

        return usr_record
    except:
        model_state[model_name]['state'] = 0
        model_state[model_name]['token'] = 0

        return {}


def test_model_proc(model_state , model_name):
    start_time = time.perf_counter()
    while True:
        try:
            conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
            conn.send(('test' , 'test'))
            conn.send(('456' , '123'))
            print(conn.recv())
            return True
        except:
            time.sleep(5)
            if start_time - time.perf_counter() > 60:
                return False

def import_user_record(model_state , model_name  , user_record):
    conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
    conn.send(('import' , 'import'))
    conn.send(user_record)
    conn.close()

def export_user_record(model_state , model_name):
    conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
    conn.send(('export' , 'export'))
    user_record = conn.recv()
    conn.close()

    return user_record


def communicate_model(model_state , model_name , user , prompt):
    conn = Client(('localhost' , model_state[model_name]['port']) , authkey=b'1234')
    conn.send((user , prompt))
    response = conn.recv()
    conn.close()
    return response

def communicate_queue(single_model_queue , model_state , model_name , current_user , thread_state ):
    while thread_state:
        if not single_model_queue.empty() and model_state[model_name]['state'] == 2:
            user_request_dic = single_model_queue.get()
            print(user_request_dic)
            current_user[model_name] = user_request_dic

            while not  test_model_proc(model_state , model_name) == True: pass

            start_time = time.perf_counter()
            res = communicate_model(model_state , model_name , user_request_dic['user'] , user_request_dic['prompt'])
            end_time = time.perf_counter()

            res.totalTime = end_time - user_request_dic['start_time']
            res.executionTime = end_time - start_time
            user_request_dic['response'] = res

            current_user[model_name] = {}