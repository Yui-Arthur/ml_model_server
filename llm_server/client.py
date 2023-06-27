from model_server_pb2 import ( modelRequest , modelResponse , modelName , modelInfo , modelConfig ,  empty , userRecord , queueSize)
from model_server_pb2_grpc import *
import grpc

# channel = grpc.insecure_channel("140.127.208.185:50051")
channel = grpc.insecure_channel("localhost:50051")
client = LLMServiceStub(channel)
user = 2
request = modelRequest(user = user , modelName = "vicuna", prompt = "Tell me about AI 123")
# rel = client.getModelResponse(request)
# rel = client.checkModelState(empty())
# rel = client.checkUSerRecord(modelName(modelName = "vicuna"))
# rel = client.createModelProc(modelConfig(modelName = "vicuna" , maxToken = 5))
rel = client.showQueurSize(modelName(modelName = "vicuna"))
# rel = client.deleteModelProc(modelName(modelName = "vicuna"))
# rel = client.showCurrentUser(modelName(modelName = "vicuna"))
print(rel)