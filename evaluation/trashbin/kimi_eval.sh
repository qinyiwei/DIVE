# few-shot for supervised fine-tuning model
export PATH="/cpfs01/user/liupengfei/ethan/miniconda3/bin:$PATH"
source activate abel

DEVICE=7
# 1
ckpts_dir="/cpfs01/shared/GAIR/GAIR_hdd/ckpts"
MODEL_NAME="tencent/hunyuan"
DEV_SET=bench_now
CUDA_VISIBLE_DEVICES=${DEVICE} python -m evaluation.inference_kimi --model_dir ${ckpts_dir}/${MODEL_NAME} --temperature 0.0 --top_p 1.0 --output_file ./outputs/${DEV_SET}/${MODEL_NAME}.jsonl --dev_set ${DEV_SET} --prompt_type few-shot

# MODEL:
# abel_plus: /cpfs01/shared/GAIR/GAIR_hdd/hyzou/math_sft    mistral-7b-sft/abel-plus_lr1e-6_ep3_part
# wizardMath: /cpfs01/shared/GAIR/GAIR_hdd/ckpts    WizardLM/WizardMath-7B-V1.0
# Abel: /cpfs01/shared/GAIR/GAIR_hdd/ckpts      Abel/GAIRMath-Abel-7b
# tencent:                                      tencent/hunyuan

# Mistral: /cpfs01/shared/GAIR/GAIR_hdd/ckpts   mistralai/Mistral-7B-v0.1
# LLaMA: /cpfs01/shared/GAIR/GAIR_hdd/ckpts     llama-2/7b
# InternLM: /cpfs01/shared/GAIR/GAIR_hdd/ckpts  internlm/internlm-7b
# Qwen: /cpfs01/shared/GAIR/GAIR_hdd/ckpts      Qwen/Qwen-7B
# Baichuan2: /cpfs01/shared/GAIR/GAIR_hdd/ckpts baichuan-inc/Baichuan2-7B-Base
# 