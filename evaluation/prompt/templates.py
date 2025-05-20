from .gsm8k import gsm8k_examples
from .math import math_examples
from .amc import amc_examples
from .gair_math import gair_math_examples_1, gair_math_examples_2
from .mathgpt import mathgpt_examples
from .mathqa import mathqa_examples
from .theoremqa import theoremqa_examples
from .svamp import svamp_examples
from .agieval_math import agieval_math_examples
from .aqua import aqua_examples
from .asdiv_a import asdiva_examples
from .mawps import mawps_examples
from .mmlu_math import mmlu_math_examples
from .numglue import numglue_examples

Instruction = '''You are an expect in mathematical reasoning. Here you are asked to answer one mathematical question starting with 'Question:'. Your answer will start with 'Answer: let's think step by step'. 

The answer needs to include necessary reasoning steps to demonstrate your thinking procedure, and the final result of your calculation is demonstrated at the end of your answer starting with '[ANSWERKEY]'. 

Here are some examples starting with 'Question: ' for your reference.
'''

Instruction = ""
agieval_math_template: str = Instruction + agieval_math_examples
aqua_template: str = Instruction + aqua_examples
asdiva_template: str = Instruction + asdiva_examples
mawps_template: str = Instruction + mawps_examples
mmlu_math_template: str = Instruction + mmlu_math_examples
numglue_template: str = Instruction + numglue_examples
amc_template: str = Instruction + amc_examples
gair_math_1_template: str = Instruction + gair_math_examples_1
gair_math_2_template: str = Instruction + gair_math_examples_2
gsm8k_template: str = Instruction + gsm8k_examples
math_template: str = Instruction + math_examples
mathgpt_template: str = Instruction + mathgpt_examples
mathqa_template: str = Instruction + mathqa_examples
theoremqa_template: str = Instruction + theoremqa_examples
svamp_template: str = Instruction + svamp_examples

templates = {
    "math-single": "",
    "amc": amc_template,
    "gair-math-1": gair_math_1_template,
    "gair-math-2": gair_math_2_template,
    "gsm8k": gsm8k_template,
    "math": math_template,
    "mathqa": mathqa_template,
    "theoremqa": theoremqa_template,
    "mathgpt": mathgpt_template,
    "svamp": svamp_template,
    'agieval-math': agieval_math_template,
    'aqua': aqua_template,
    'asdiv-a': asdiva_template,
    'mawps': mawps_template,
    'mmlu-math': mmlu_math_template,
    'numglue': numglue_template,
}

