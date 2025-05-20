import jsonlines
import os
from .templates import templates

InstructionList = {
    "normal": "Question:\n[INPUT]\nLet's think step by step.\nAnswer:\n",
    "sft": "Question:\n[INPUT]\nAnswer:\nLet's think step by step.\n",
    "wizard": "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n[INPUT]\n\n### Response: Let's think step by step."
}

def get_prompts(dev_set, prompt_type, answer_key, instruction_type):
    data = []
    if os.path.isfile(dev_set):
        f = open(dev_set) 
    else:
        f = open(r"./data/test/{}.jsonl".format(dev_set))
        
    for line in jsonlines.Reader(f):
        data.append(line)
    f.close()

    prompt_list = []
    for line in data:
        source = line['source'].lower()
        if prompt_type == 'few-shot':
            if source in ['gsm8k_augment', 'gsm8k_robust', 'gsm8k_original', "gsm8k_train"]:
                prompt = templates['gsm8k']
            elif source in ['math_original', 'math_augment', 'math_sub']:
                prompt = templates['math']
            else:
                prompt = templates[source]
        elif prompt_type == 'zero-shot':
            prompt = templates["math-single"]
        else:
            raise NotImplementedError
        processed_prompt = prompt.replace("[ANSWERKEY]", answer_key)
        processed_prompt = processed_prompt + InstructionList[instruction_type]
        processed_prompt = processed_prompt.replace("[INPUT]", line['question'])
        # print(processed_prompt)
        for _ in range(1):
            prompt_list.append(processed_prompt)
    # print(processed_prompt)
    return prompt_list, data
