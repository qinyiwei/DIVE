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
from evaluation.math_normalization import *
from evaluation.constants import *
from openai import OpenAI

DEVSET = ['gsm8k', 'math', 'mathgpt', 'gsm8k_robust', 'mathqa', 'mmlu']

def test_answer(pred_str, ans_str):
    pattern = "#### (.*)$"
    if "Question" in pred_str:
        pred_str = pred_str.split("Question")[0]
    pred_str = pred_str.strip()
    preds = re.findall(pattern, pred_str)
    pred = preds[-1] if len(preds) >= 1 else ""
    if "</s>" in pred:
        pred = pred[:-4]
    gold = ans_str
    pred = normalize_final_answer(pred)
    gold = normalize_final_answer(gold)
    return check_sympy_equivalence(gold, pred), pred, gold



def parser_pred_ans(preds_str, golds_str, properties_list):
    num_q, acc = 0, 0
    results, preds, golds = [], [], []
    correct_table, cnt_table = {}, {}
    source_set = set()
    for pred_str, gold_str, properties in tqdm(zip(preds_str, golds_str, properties_list), total=len(preds_str)):
        num_q += 1
        result, pred, gold = test_answer(pred_str, gold_str)
        results.append(result)
        preds.append(pred)
        golds.append(gold)
        acc = (acc + 1) if result else acc
        source, tag = properties['source'], properties['tag']
        source_set.add(source)
        if source not in correct_table.keys():
            correct_table[source] = 1 if result else 0
            cnt_table[source] = 1
        else:
            correct_table[source] = (correct_table[source] + 1) if result else correct_table[source]
            cnt_table[source] += 1
        for key in tag.keys():
                value = tag[key]
                value = source+","+key+"__"+value
                if value not in correct_table.keys():
                    correct_table[value] = 1 if result else 0
                    cnt_table[value] = 1
                else:
                    correct_table[value] = (correct_table[value] + 1) if result else correct_table[value]
                    cnt_table[value] += 1
    print('num_q %d correct %d ratio %.4f' % (num_q, acc, float(acc / num_q)))
    acc_table = {}
    for key in correct_table.keys():
        acc_table[key] = correct_table[key] / cnt_table[key]
    acc_table = list(zip(acc_table.keys(), acc_table.values()))
    acc_table.sort(key=lambda x: x[0])
    for key, acc in acc_table:
        if key in source_set:
            print(key+" : "+str(acc))
        else:
            print("    " + key.split(",")[-1]+ " : " + str(acc))
    return results, preds, golds



def get_results(pred_file, dev_set):
    if dev_set != "":
        golds_str = []
        properties = []
        with open(f'./data/test/bench.jsonl', 'r', encoding='utf-8') as f:
            target_data = [line for line in jsonlines.Reader(f)]
            golds_str = [line['answer'] for line in target_data]
            properties = [{"source":line['source'], "tag":line['tag']} for line in target_data]
        preds_str = []
        with open(pred_file, 'r', encoding='utf-8') as f:
            pred_data = [line for line in jsonlines.Reader(f)]
            preds_str = [line['response'] for line in pred_data]
        results, preds, golds = parser_pred_ans(preds_str, golds_str, properties)
        for i, line in enumerate(pred_data):
            line['pred'] = preds[i]
            line['gold'] = golds[i]
            line['result'] = results[i]
        with open(pred_file, 'w', encoding='utf-8') as f:
            for line in pred_data:
                f.write(json.dumps(line) + '\n')

prompt_mapping = {
    "math-single": "Question:\n{input}\nAnswer:\nLet's think step by step.\n",
    "gsm8k-demos": Prompt_gsm8k,
    "math-demos": Prompt_math,
    "amc-demos": Prompt_amc,
    "mathgpt-demos": Prompt_mathgpt,
    "gair-math-demos": Prompt_gair_math,
    "theoremqa-demos": Prompt_theoremqa,
}

def get_inputs(dev_set):
    data = []
    with open(f"./data/test/bench.jsonl") as f:
        for line in jsonlines.Reader(f):
            data.append(line)
            data = [line for line in data]
    prompt_list = []
    for line in data:
        source = line['source']
        if 'gsm8k' in source:
            prompt = prompt_mapping['gsm8k-demos']
        elif 'mathgpt' in source:
            prompt = prompt_mapping['mathgpt-demos']
        elif 'math' in source:
            prompt = prompt_mapping['math-demos']
        elif 'amc' in source:
            prompt = prompt_mapping['amc-demos']
        elif 'gair-math' in source:
            prompt = prompt_mapping['gair-math-demos']
        elif 'theoremqa' in source:
            prompt = prompt_mapping['theoremqa-demos']
        else:
            prompt = prompt_mapping['math-single']
        processed_prompt = prompt.replace("[INPUT]", line['question'])
        prompt_list.append(processed_prompt)
    return prompt_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, required=True)
    parser.add_argument('--max_tokens', type=int, default=4096)
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--top_p', type=float, default=1.0)
    parser.add_argument('--presence_penalty', type=float, default=0.0)
    parser.add_argument('--frequency_penalty', type=float, default=0.0)
    parser.add_argument('--output_file_name', type=str, default='output.json')
    parser.add_argument('--stop', type=str, nargs='+', default=['Question'], help="you can pass one or multiple stop strings to halt the generation process.")
    parser.add_argument('--dev_set', type=str, default='all')
    parser.add_argument('--prompt_type', type=str, default='math-single')
    parser.add_argument('--sample_num', type=int, default=-1, )
    parser.add_argument('--eval_only', type=bool, default=False)
    parser.add_argument('--max_num_batched_tokens', type=int, default=32768)
    args = parser.parse_args()
    # key=Y2xjNnFlZDB0YzE3OGtuMmdkN2c6bXNrLUZUSHJDQjV3dzQ0c29sczRyWlVTazhGbjdLbHU=

    if args.eval_only == False:
        # num_gpus = torch.cuda.device_count()
        # another_args = {'max_num_batched_tokens': args.max_num_batched_tokens}
        # llm = LLM(model=args.model_dir, tensor_parallel_size=num_gpus, **another_args, trust_remote_code=True)
        client = OpenAI(api_key="Y2xjNnFlZDB0YzE3OGtuMmdkN2c6bXNrLUZUSHJDQjV3dzQ0c29sczRyWlVTazhGbjdLbHU=",base_url="https://api.moonshot.cn/v1")
        print(">>>>>> model loaded")

        sampling_params = SamplingParams(temperature=args.temperature, top_p=args.top_p, max_tokens=args.max_tokens,
            stop=args.stop, presence_penalty=args.presence_penalty, frequency_penalty=args.frequency_penalty)
        
        processed_prompts = get_inputs(args.dev_set)
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
        # sorted_outputs = sorted(outputs, key=lambda output: int(output.request_id))
        print(">>>>>> generation done")


        if not os.path.exists(os.path.dirname(args.output_file_name)):
            os.makedirs(os.path.dirname(args.output_file_name))
        with open(args.output_file_name, 'w') as f:
            for id, output in enumerate(outputs):
                f.write(json.dumps({'id':id, 'prompt': output['prompt'], 'response':output['response'].choices[0].message.content}) + '\n')
        print('>>>>>> writing prediction done')

    get_results(args.output_file_name, args.dev_set)
    print(">>>>> evaluation done")