# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import model_server_pb2 as model__server__pb2


class LLMServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getModelResponse = channel.unary_unary(
                '/LLMService/getModelResponse',
                request_serializer=model__server__pb2.modelRequest.SerializeToString,
                response_deserializer=model__server__pb2.modelResponse.FromString,
                )
        self.deleteModelProc = channel.unary_unary(
                '/LLMService/deleteModelProc',
                request_serializer=model__server__pb2.modelName.SerializeToString,
                response_deserializer=model__server__pb2.modelInfo.FromString,
                )
        self.createModelProc = channel.unary_unary(
                '/LLMService/createModelProc',
                request_serializer=model__server__pb2.modelConfig.SerializeToString,
                response_deserializer=model__server__pb2.modelInfo.FromString,
                )
        self.checkModelState = channel.unary_unary(
                '/LLMService/checkModelState',
                request_serializer=model__server__pb2.empty.SerializeToString,
                response_deserializer=model__server__pb2.modelInfo.FromString,
                )
        self.checkUSerRecord = channel.unary_unary(
                '/LLMService/checkUSerRecord',
                request_serializer=model__server__pb2.modelName.SerializeToString,
                response_deserializer=model__server__pb2.userRecord.FromString,
                )
        self.showQueurSize = channel.unary_unary(
                '/LLMService/showQueurSize',
                request_serializer=model__server__pb2.modelName.SerializeToString,
                response_deserializer=model__server__pb2.queueSize.FromString,
                )
        self.showCurrentUser = channel.unary_unary(
                '/LLMService/showCurrentUser',
                request_serializer=model__server__pb2.modelName.SerializeToString,
                response_deserializer=model__server__pb2.currentUser.FromString,
                )


class LLMServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getModelResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteModelProc(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createModelProc(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkModelState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def checkUSerRecord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def showQueurSize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def showCurrentUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LLMServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getModelResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.getModelResponse,
                    request_deserializer=model__server__pb2.modelRequest.FromString,
                    response_serializer=model__server__pb2.modelResponse.SerializeToString,
            ),
            'deleteModelProc': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteModelProc,
                    request_deserializer=model__server__pb2.modelName.FromString,
                    response_serializer=model__server__pb2.modelInfo.SerializeToString,
            ),
            'createModelProc': grpc.unary_unary_rpc_method_handler(
                    servicer.createModelProc,
                    request_deserializer=model__server__pb2.modelConfig.FromString,
                    response_serializer=model__server__pb2.modelInfo.SerializeToString,
            ),
            'checkModelState': grpc.unary_unary_rpc_method_handler(
                    servicer.checkModelState,
                    request_deserializer=model__server__pb2.empty.FromString,
                    response_serializer=model__server__pb2.modelInfo.SerializeToString,
            ),
            'checkUSerRecord': grpc.unary_unary_rpc_method_handler(
                    servicer.checkUSerRecord,
                    request_deserializer=model__server__pb2.modelName.FromString,
                    response_serializer=model__server__pb2.userRecord.SerializeToString,
            ),
            'showQueurSize': grpc.unary_unary_rpc_method_handler(
                    servicer.showQueurSize,
                    request_deserializer=model__server__pb2.modelName.FromString,
                    response_serializer=model__server__pb2.queueSize.SerializeToString,
            ),
            'showCurrentUser': grpc.unary_unary_rpc_method_handler(
                    servicer.showCurrentUser,
                    request_deserializer=model__server__pb2.modelName.FromString,
                    response_serializer=model__server__pb2.currentUser.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LLMService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LLMService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getModelResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/getModelResponse',
            model__server__pb2.modelRequest.SerializeToString,
            model__server__pb2.modelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteModelProc(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/deleteModelProc',
            model__server__pb2.modelName.SerializeToString,
            model__server__pb2.modelInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createModelProc(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/createModelProc',
            model__server__pb2.modelConfig.SerializeToString,
            model__server__pb2.modelInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkModelState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/checkModelState',
            model__server__pb2.empty.SerializeToString,
            model__server__pb2.modelInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def checkUSerRecord(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/checkUSerRecord',
            model__server__pb2.modelName.SerializeToString,
            model__server__pb2.userRecord.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def showQueurSize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/showQueurSize',
            model__server__pb2.modelName.SerializeToString,
            model__server__pb2.queueSize.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def showCurrentUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LLMService/showCurrentUser',
            model__server__pb2.modelName.SerializeToString,
            model__server__pb2.currentUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
