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
from .prompt import get_prompts
from .eval import get_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, default="./")
    parser.add_argument('--output_file_name', type=str, default='output.json')
    parser.add_argument('--dev_set', type=str, default='all')
    parser.add_argument('--prompt_type', type=str, default='few-shot')
    parser.add_argument('--answer_key', type=str, default='####')
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
    parser.add_argument('--max_num', type=int, default=None)
    args = parser.parse_args()


    if args.eval_only == False:
        model = Models[args.model_type](args)
        processed_prompts, test_data = get_prompts(args.dev_set, args.prompt_type, args.answer_key, args.instruction_type)
        if args.max_num is not None:
            processed_prompts = processed_prompts[:args.max_num]
        print(processed_prompts[:5])
        sorted_outputs = model.generate(processed_prompts)
        print(sorted_outputs[:5])
        if not os.path.exists(os.path.dirname(args.output_file_name)):
            os.makedirs(os.path.dirname(args.output_file_name))
        with open(args.output_file_name, 'w') as f:
            for id, (output, test_data_line) in enumerate(zip(sorted_outputs, test_data)):
                if args.model_type == "api":
                    data = {'id':id, 'prompt': output['prompt'], 'response':output['response']}
                else:
                    data = {'id':id, 'prompt': output.prompt, 'response':output.outputs[0].text.strip().strip(".")}
                if "subject" in test_data_line:
                    data["subject"] = test_data_line["subject"]
                if "level" in test_data_line:
                    data["level"] = test_data_line["level"]
                if "solution" in test_data_line:
                    data["gt_solution"] = test_data_line["solution"]
                if "unique_id" in test_data_line:
                    data["unique_id"] = test_data_line["unique_id"]
                if "question" in test_data_line:
                    data["question"] = test_data_line["question"]

                f.write(json.dumps(data) + '\n')
        print('>>>>>> writing prediction done')
        
    get_results(args.output_file_name, args.dev_set, args.answer_key)
    print(">>>>> evaluation done")
