from multiprocessing.connection import Listener
from model_server_pb2 import ( modelRequest , modelResponse )
import argparse

address = ('localhost', 9001)   


class vicuna:
    def __init__(self , max_token = 150):
        from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
        from transformers import AutoTokenizer, logging, pipeline
        from transformers import TextGenerationPipeline
        
        model_id = "TheBloke/vicuna-7B-1.1-GPTQ-4bit-128g"
        model_basename="vicuna-7B-1.1-GPTQ-4bit-128g.no-act-order"

        model = AutoGPTQForCausalLM.from_quantized(model_id,device="cuda:0",use_safetensors=False, quantize_config=None, model_basename=model_basename)

        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)

        self.pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer, device="cuda:0" , max_new_tokens = max_token)
        self.user_record = {}

    def generation(self , user , prompt):

        if user not in self.user_record.keys():
            self.user_record[user] = ""
        
        prompt_format = self.user_record[user] + f"""HUMAN: {prompt}
ASSISTANT:"""

        response = self.pipeline(prompt_format)[0]["generated_text"]

        self.user_record[user] += response + "\n"
        
        return  response

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-tokens', nargs='?', type=int, default=150, help='max_new_tokens')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()
    model = vicuna(opt.max_tokens)

    with Listener(address, authkey=b'1234') as listener:
        
        while True:
            conn = listener.accept()
            usr , prompt = conn.recv()

            print(usr , prompt)
            if usr == 'del':
                conn.send("ok")
                break
            
            response = model.generation(usr , prompt)
            # response = "1234"
            conn.send(modelResponse(prompt = prompt , response = response))
            conn.close()
