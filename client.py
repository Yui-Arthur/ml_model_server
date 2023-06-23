from model_server_pb2 import ( modelRequest , modelResponse )
from model_server_pb2_grpc import *
import grpc

channel = grpc.insecure_channel("localhost:50051")
client = sendToModelStub(channel)
request = modelRequest(user = 1 , modelName = "vicuna", prompt = "What gift would my girlfriend like")
rel = client.getModelResponse(request)
print(rel)