from model_server_pb2 import ( modelRequest , modelResponse , modelName , modelInfo , modelConfig)
from model_server_pb2_grpc import *
import grpc

channel = grpc.insecure_channel("localhost:50051")
client = sendToModelStub(channel)
user = 1
request = modelRequest(user = user , modelName = "vicuna", prompt = "What gift would my girlfriend like")
rel = client.getModelResponse(request)
# rel = client.checkModelState(modelName(modelName = "vicuna"))
# rel = client.createModelProc(modelConfig(modelName = "vicuna" , maxToken = 5))
# rel = client.deleteModelProc(modelName(modelName = "vicuna"))
print(rel)