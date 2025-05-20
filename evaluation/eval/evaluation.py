import jsonlines
import json
import os
from tqdm import tqdm
from .math_normalization import *
import pdb

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

def test_answer(pred_str, ans_str, answer_key):
    pred = get_answer_from_response(pred_str, answer_key)
    gold = normalize_final_answer(ans_str)
    return check_sympy_equivalence(gold, pred), pred, gold


def parser_pred_ans(preds_str, golds_str, properties_list, answer_key):
    num_q, acc = 0, 0
    results, preds, golds = [], [], []
    correct_table, cnt_table = {}, {}
    source_set = set()
    for pred_str, gold_str, properties in tqdm(zip(preds_str, golds_str, properties_list), total=len(preds_str)):
        num_q += 1
        result, pred, gold = test_answer(pred_str, gold_str, answer_key)
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
                value = source+","+str(key)+"__"+str(value)
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
            print(key.lower()+" : "+str(acc))
        else:
            print("    " + key.split(",")[-1]+ " : " + str(acc))
    return results, preds, golds

def get_results(pred_file, dev_set, answer_key):
    print("--------------")
    if dev_set != "":
        golds_str = []
        properties = []
        
        if os.path.isfile(dev_set):
            f = open(dev_set, encoding='utf-8') 
        else:
            f = open(r"./data/test/{}.jsonl".format(dev_set), encoding='utf-8')
        target_data = [line for _ in range(1) for line in jsonlines.Reader(f)]
        golds_str = [line['answer'] for line in target_data]
        properties = [{"source":line['source'], "tag":line['tag']} for line in target_data]
        f.close()

        preds_str = []
        with open(pred_file, 'r', encoding='utf-8') as f:
            pred_data = [line for line in jsonlines.Reader(f)]
            preds_str = [line['response'] for line in pred_data]
        results, preds, golds = parser_pred_ans(preds_str, golds_str, properties, answer_key)
        for i, line in enumerate(pred_data):
            line['pred'] = preds[i]
            line['gold'] = golds[i]
            line['result'] = results[i]
        with open(pred_file, 'w', encoding='utf-8') as f:
            for line in pred_data:
                f.write(json.dumps(line) + '\n')