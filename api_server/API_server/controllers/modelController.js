var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');
const protoFile = 'proto/model_server.proto';
const packageDefinitionProc = protoLoader.loadSync(protoFile);
const processingProto = grpc.loadPackageDefinition(packageDefinitionProc);
var client = new processingProto.sendToModel('llm_server:50051', grpc.credentials.createInsecure())

const checkModel = async (req, res) => {


    let modelName = req.params.modelName;
    console.log(req.params.modelName);
    client.checkModelState({modelName:modelName} , function(err , response){
        if(err){
            console.log(err);
            res.status(400).send("error");
        }
        else{
            console.log(response.modelInfo);
            res.status(200).send(response.modelInfo);
        }
    });
}

const createModel = async (req, res) => {

    let modelName = req.params.modelName;
    let maxToken = req.params.maxToken;
    client.createModelProc({modelName:modelName, maxToken:maxToken} , function(err , response){
        if(err){
            console.log(err);
            res.status(400).send("error")
        }
        else{
            console.log(response.modelInfo);
            res.status(200).send(response.modelInfo);
        }
    });
}

const deleteModel = async (req, res) => {
    
    let modelName = req.params.modelName;
    client.deleteModelProc({modelName:modelName} , function(err , response){
        if(err){
            console.log(err);
            res.status(400).send("error")
        }
        else{
            console.log(response.modelInfo);
            res.status(200).send(response.modelInfo);
        }
    })
}

const getModel = async (req, res) => {

    let prompt = req.body.prompt;
    let modelName = req.params.modelName;
    let user = req.params.user;
    
    client.getModelResponse({user: user, modelName: modelName, prompt: prompt} , function(err , response){
        if(err){
            console.log(err);
            res.status(400).send("error")
        }
        else{
            console.log(response.response);
            res.status(200).send(response);
        }
    })
}


module.exports = {
    checkModel,
    createModel,
    deleteModel,
    getModel
}