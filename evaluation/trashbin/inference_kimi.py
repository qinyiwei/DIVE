from vllm import LLM, SamplingParams
import os
import re
import json
import jsonlines
import argparse
import torch
from tqdm import tqdm
import sys
import pdb
from openai import OpenAI
from .model import Models
from .prompt import get_prompts
from .eval import get_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, default="./")
    parser.add_argument('--output_file_name', type=str, default='output.json')
    parser.add_argument('--dev_set', type=str, default='all')
    parser.add_argument('--prompt_type', type=str, default='few-shot')
    parser.add_argument('--model_type', type=str, default='vllm')
    parser.add_argument('--trust_remote_code', type=bool, default=True)
    parser.add_argument('--max_tokens', type=int, default=4096)
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--top_p', type=float, default=1.0)
    parser.add_argument('--presence_penalty', type=float, default=0.0)
    parser.add_argument('--frequency_penalty', type=float, default=0.0)
    parser.add_argument('--stop', type=str, nargs='+', default=['Question'], help="you can pass one or multiple stop strings to halt the generation process.")
    parser.add_argument('--max_num_batched_tokens', type=int, default=32768)

    parser.add_argument('--eval_only', type=bool, default=False)
    args = parser.parse_args()

    if args.eval_only == False:
        client = OpenAI(api_key="Y2xjNnFlZDB0YzE3OGtuMmdkN2c6bXNrLUZUSHJDQjV3dzQ0c29sczRyWlVTazhGbjdLbHU=",base_url="https://api.moonshot.cn/v1")
        
        processed_prompts = get_prompts(args.dev_set, args.prompt_type)
        outputs = []
        for prompt in tqdm(processed_prompts):
            output = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[ 
                    {"role": "system", "content": "You are an AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,)
            outputs.append({"prompt": prompt, "response":output})
        print(">>>>>> generation done")

        if not os.path.exists(os.path.dirname(args.output_file_name)):
            os.makedirs(os.path.dirname(args.output_file_name))
        with open(args.output_file_name, 'w') as f:
            for id, output in enumerate(outputs):
                f.write(json.dumps({'id':id, 'prompt': output['prompt'], 'response':output['response'].choices[0].message.content}) + '\n')
        print('>>>>>> writing prediction done')

    get_results(args.output_file_name, args.dev_set)
    print(">>>>> evaluation done")