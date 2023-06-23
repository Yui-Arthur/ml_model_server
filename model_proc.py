from multiprocessing.connection import Listener
from model_server_pb2 import ( modelRequest , modelResponse )

address = ('localhost', 9001)   


class vicuna:
    def __init__(self):
        from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
        from transformers import AutoTokenizer, logging, pipeline
        from transformers import TextGenerationPipeline
        
        model_id = "TheBloke/vicuna-7B-1.1-GPTQ-4bit-128g"
        model_basename="vicuna-7B-1.1-GPTQ-4bit-128g.no-act-order"

        model = AutoGPTQForCausalLM.from_quantized(model_id,device="cuda:0",use_safetensors=False, quantize_config=None, model_basename=model_basename)

        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)

        self.pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer, device="cuda:0" , max_new_tokens = 20)

    def generation(self , prompt):
        prompt_format = f'''### Human: {prompt}
### Assistant:'''
        return self.pipeline(prompt_format)[0]["generated_text"]


model = vicuna()

with Listener(address, authkey=b'1234') as listener:
    
    while True:
        conn = listener.accept()
        usr , prompt = conn.recv()

        if usr == 'del':
            conn.send("ok")
            break
        
        response = model.generation(prompt)
        # response = "1234"
        conn.send(modelResponse(prompt = "yes" , response = response))
        conn.close()
        # print('connection accepted from', listener.last_accepted)

        #  conn.recv()