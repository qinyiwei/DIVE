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
import warnings
warnings.filterwarnings("ignore")

from .model import Models
from .eval import get_preference

import jsonlines
import os

InstructionList = {
    "normal": "Question:\n[INPUT]\nLet's think step by step.\nAnswer:\n",
    "sft": "Question:\n[INPUT]\nAnswer:\nLet's think step by step.\n",
    "wizard": "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n[INPUT]\n\n### Response: Let's think step by step."
}

def get_prompts(dev_set, prompt_type, instruction_type):
    data = []
    if os.path.isfile(dev_set):
        f = open(dev_set) 
    else:
        f = open(r"./data/test/{}.jsonl".format(dev_set))
    
    reader = jsonlines.Reader(f)
    for line in tqdm(reader, desc="Reading lines"):
        data.append(line)

    f.close()

    prompt_list = []
    answer_list = []
    for line in data:
        processed_prompt = ""
        processed_prompt = processed_prompt + InstructionList[instruction_type]
        processed_prompt = processed_prompt.replace("[INPUT]", line['question'])
        # print(processed_prompt)
        for _ in range(1):
            prompt_list.append(processed_prompt)
        answer_list.append(line["answer"])
    # print(processed_prompt)
    return prompt_list,answer_list

CHUNK_SIZE = 1000
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, default="./")
    parser.add_argument('--output_file_name', type=str, default='output.json')
    parser.add_argument('--dev_set', type=str, default='all')
    parser.add_argument('--prompt_type', type=str, default='few-shot')
    parser.add_argument('--instruction_type', type=str, default='normal')
    parser.add_argument('--model_type', type=str, default='vllm')
    parser.add_argument('--trust_remote_code', type=bool, default=True)
    parser.add_argument('--max_tokens', type=int, default=4096)
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--top_p', type=float, default=1.0)
    parser.add_argument('--presence_penalty', type=float, default=0.0)
    parser.add_argument('--frequency_penalty', type=float, default=0.0)
    parser.add_argument('--stop', type=str, nargs='+', default=['Question', '#'], help="you can pass one or multiple stop strings to halt the generation process.")
    parser.add_argument('--max_num_batched_tokens', type=int, default=32768)
    parser.add_argument('--eval_only', type=bool, default=False)
    parser.add_argument('--sampling_num', type=int, default=10)
    parser.add_argument('--num_pos', type=int, default=2)
    parser.add_argument('--num_neg', type=int, default=2)
    args = parser.parse_args()

    if args.eval_only == False:
        model = Models[args.model_type](args)
        processed_prompts,gold_answers = get_prompts(args.dev_set, args.prompt_type, args.instruction_type)
        
        if not os.path.exists(os.path.dirname(args.output_file_name)):
            os.makedirs(os.path.dirname(args.output_file_name))

        with open(args.output_file_name, 'w') as f:
            for ch in range(0, len(processed_prompts), CHUNK_SIZE):
                print("chunk {}/{}".format(ch/CHUNK_SIZE, len(processed_prompts)/CHUNK_SIZE))
                prompts_chunk = processed_prompts[ch:ch + CHUNK_SIZE]
                gold_answers_chunk = gold_answers[ch:ch + CHUNK_SIZE]

                sorted_outputs = []
                for _ in range(args.sampling_num):
                    sorted_outputs.append(model.generate(prompts_chunk))

                for id, prompt, gold_answer in zip(range(len(sorted_outputs[0])), prompts_chunk, gold_answers_chunk):
                    responses=[]
                    for sampleId in range(len(sorted_outputs)):
                        output=sorted_outputs[sampleId][id]
                        if args.model_type == "api":
                            responses.append(output['response'])
                        else:
                            prob=output.outputs[0].cumulative_logprob/len(output.outputs[0].token_ids)
                            responses.append((output.outputs[0].text.strip().strip("."),prob))
                    f.write(json.dumps({'id':id, 'prompt': prompt, 'responses':responses, 'answer': gold_answer}) + '\n')
                    f.flush()
        print('>>>>>> writing prediction done')
        print(">>>>>> writing file to {}".format(args.output_file_name))
    