#same as get_preference_data13

import jsonlines
import json
import os
from tqdm import tqdm
import pdb
import random
import argparse
# Part of the code is modified from the code snippets provided in "Solving Quantitative Reasoning Problems with Language Models" by Lewkowycz et al.
import pdb
import re
import sympy
import threading
from sympy.parsing.latex import parse_latex

import numpy as np
import matplotlib.pyplot as plt
import math

import numpy as np

SUBSTITUTIONS = [
    ('an ', ''), ('a ', ''), ('.$', '$'), ('\\$', ''), (r'\ ', ''), ('\%', '%'),
    (' ', ''), ('mbox', 'text'), (',\\text{and}', ','),
    ('\\text{and}', ','), ('\\text{m}', '\\text{}')
]
REMOVED_EXPRESSIONS = [
    'square', 'ways', 'integers', 'dollars', 'mph', 'inches', 'ft',
    'hours', 'km', 'units', '\\ldots', 'sue', 'points', 'feet',
    'minutes', 'digits', 'cents', 'degrees', 'cm', 'gm', 'pounds',
    'meters', 'meals', 'edges', 'students', 'childrentickets', 'multiples',
    '\\text{s}', '\\text{.}', '\\text{\ns}', '\\text{}^2',
    '\\text{}^3', '\\text{\n}', '\\text{}', r'\mathrm{th}',
    r'^\circ', r'^{\circ}', r'\;', r',\!', '{,}', '"', '\\dots'
]

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def normalize_final_answer(final_answer: str) -> str:
    """Normalize a final answer to a quantitative reasoning question."""
    final_answer = str(final_answer).split('=')[-1]

    for before, after in SUBSTITUTIONS:
        final_answer = final_answer.replace(before, after)
    for expr in REMOVED_EXPRESSIONS:
        final_answer = final_answer.replace(expr, '')

    # Extract answer that is in LaTeX math, is bold,
    # is surrounded by a box, etc.
    final_answer = re.sub(r'(.*?)(\$)(.*?)(\$)(.*)', '$\\3$', final_answer)
    final_answer = re.sub(r'(\\text\{)(.*?)(\})', '\\2', final_answer)
    final_answer = re.sub(r'(\\textbf\{)(.*?)(\})', '\\2', final_answer)
    final_answer = re.sub(r'(\\overline\{)(.*?)(\})', '\\2', final_answer)
    final_answer = re.sub(r'(\\boxed\{)(.*)(\})', '\\2', final_answer)

    # Normalize shorthand TeX:
    # \fracab -> \frac{a}{b}
    # \frac{abc}{bef} -> \frac{abc}{bef}
    # \fracabc -> \frac{a}{b}c
    # \sqrta -> \sqrt{a}
    # \sqrtab -> sqrt{a}b
    final_answer = re.sub(
        r'(frac)([^{])(.)', 'frac{\\2}{\\3}', final_answer)
    final_answer = re.sub(
        r'(sqrt)([^{])', 'sqrt{\\2}', final_answer)
    final_answer = final_answer.replace('$', '')

    # Normalize 100,000 -> 100000
    if final_answer.replace(',', '').isdigit():
        final_answer = final_answer.replace(',', '')
    # 3.0 -> 3
    if final_answer.endswith(".0") and final_answer[:-2].isdigit():
        final_answer = final_answer[:-2]
    # 3.00 -> 3
    if final_answer.endswith(".00") and final_answer[:-3].isdigit():
        final_answer = final_answer[:-3]
    if final_answer.endswith("%") and final_answer[:-1].isdigit():
        final_answer = final_answer[:-1]
    # A -> a
    if final_answer.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        final_answer = final_answer.lower()
    return final_answer

def check_sympy_equivalence(formatted_target_str, formatted_prediction_str):
    flag = False    
    try:
        target_expr = parse_latex(formatted_target_str)
    except:
        target_expr = formatted_target_str
        flag = True
    
    try:
        prediction_expr = parse_latex(formatted_prediction_str)
    except:
        prediction_expr = formatted_prediction_str
        flag = True
    
    if flag == True:
        return formatted_target_str == formatted_prediction_str

    try:
        return sympy.simplify(target_expr - prediction_expr) == 0
    except:
        return False
    
def last_boxed_only_string(string):
    idx = string.rfind('\\boxed')
    if idx < 0:
        idx = string.rfind('\\fbox')
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == '{':
            num_left_braces_open += 1
        if string[i] == '}':
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    if right_brace_idx is None:
        retval = None
    else:
        retval = string[idx:right_brace_idx + 1]

    return retval


def remove_boxed(s):
    left = '\\boxed{'
    try:
        assert s[:len(left)] == left
        assert s[-1] == '}'
        return s[len(left):-1]
    except Exception:
        return None


def extract_boxed_answer(pred_str, strip_double_curly_brace=False):
    boxed_str = last_boxed_only_string(pred_str)
    if boxed_str is None:
        return None
    answer = remove_boxed(boxed_str)
    if answer is None:
        return None
    if strip_double_curly_brace:
        match = re.match('^\{(.*)\}$', answer)  # noqa: W605
        if match:
            answer = match.group(1)
    return answer

def test_answer(pred_str, ans_str, answer_key):
    pred = get_answer_from_response(pred_str, answer_key)
    gold = get_answer_from_response(ans_str, answer_key)
    return check_sympy_equivalence(gold, pred), pred, gold

def get_answer_from_response(response, answer_key):
    if answer_key == "####":
        pattern = "{} (.*)$".format(answer_key)
    elif answer_key == "# Answer":
        pattern = "{}\n\n(.*)$".format(answer_key)
    elif answer_key == "boxed":
        pass
    else:
        raise ValueError(
                f"Unknown answer_key type: {answer_key}. Should be one of ['####', 'boxed', '# Answer']"
            )
    if "Question" in response:
        response = response.split("Question")[0]
    response = response.strip()
    if answer_key == "####" or answer_key == "# Answer":
        preds = re.findall(pattern, response)
        pred = preds[-1] if len(preds) >= 1 else ""
        if "</s>" in pred:
            pred = pred[:-4]
    else:
        pred = extract_boxed_answer(response)

    answer = normalize_final_answer(pred)
    return answer


def parser_pred_ans(preds_strs, golds_str, answer_key, num_pair):
    preferences = []
    correct_distribution = {i:0 for i in range(len(preds_strs[0])+1)}
    pos_total=0
    neg_total=0
    model=None
    
    for pred_strs, gold_str in tqdm(zip(preds_strs, golds_str), total=len(preds_strs)):
        num_pos = 0
        num_neg = 0
        cur_pos = []
        cur_neg = []

        for pred_str in pred_strs:
            if isinstance(pred_str,str):
                result, pred, gold = test_answer(pred_str, gold_str, answer_key)
            else:
                result, pred, gold = test_answer(pred_str[0], gold_str, answer_key)

            if result:
                num_pos+=1
                cur_pos.append(pred_str)
            else:
                num_neg+=1
                cur_neg.append(pred_str)
        
        pos_total+=num_pos
        neg_total+=num_neg
        
        
        correct_distribution[num_pos]+=1

        random.shuffle(cur_pos)
        random.shuffle(cur_neg)
        if len(cur_pos)>0 and isinstance(cur_pos[0], list):
            cur_pos=[example[0] for example in cur_pos]
        if len(cur_neg)>0 and isinstance(cur_neg[0], list):
            cur_neg=[neg[0] for neg in cur_neg]

        preference = []

        for pos, neg in zip(cur_pos, cur_neg):
            pos_coef = len(cur_pos)
            neg_coef = len(cur_neg)
            preference.append([pos, neg, pos_coef, neg_coef])

        preferences.append(preference)
        
    assert len(preferences) == len(preds_strs)
    print("correct_distribution")
    print(correct_distribution)
    print("total_pos:{},total_neg:{},correct_ration:{}".format(pos_total, neg_total, pos_total/(pos_total+neg_total)))
    return preferences

def get_preference(pred_file, answer_key, output_file_append, num_pair):
    print("--------------")

    golds_str = []

    preds_strs = []
    with open(pred_file, 'r', encoding='utf-8') as f:
        pred_data = [line for line in jsonlines.Reader(f)]
        preds_strs = [line['responses'] for line in pred_data]
        golds_str = [line['answer'] for line in pred_data]


    preferences = parser_pred_ans(preds_strs, golds_str, answer_key, num_pair)

    preference_data = []
    assert len(preferences) == len(pred_data)
    for line,preference in zip(pred_data,preferences):
        query = line["prompt"]
        if len(preference)!=0:
            for one_preference in preference:
                preference_data.append(
                    {"instruction":query,
                    "output":[one_preference[0],one_preference[1]],
                    "num_crt": one_preference[2],
                    "num_wrg": one_preference[3]
                    }
                )
    preference_file=pred_file.replace(".jsonl",f"_{output_file_append}.jsonl")
    with open(preference_file, 'w', encoding='utf-8') as f:
        for line in preference_data:
            f.write(json.dumps(line) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred_file', type=str)
    parser.add_argument('--fix_pair', type=int, default=2)
    parser.add_argument('--answer_key', type=str, default='####')
    parser.add_argument('--output_file_append', type=str, default='_preference')
    args = parser.parse_args()

    get_preference(args.pred_file, args.answer_key, args.output_file_append, args.fix_pair)


