# few-shot for unsupervised fine-tuning model
export PATH="/cpfs01/user/liupengfei/ethan/miniconda3/bin:$PATH"
source activate abel

DEVICES=1
ckpts_dir="/cpfs01/shared/GAIR/GAIR_hdd/hyzou/math_sft/"
MODEL_NAME="mistral-7b-sft/abel-plus_lr1e-6_ep3_part"
DEV_SET=gsm8k
CUDA_VISIBLE_DEVICES=${DEVICES} python -m evaluation.inference --model_dir ${ckpts_dir}/${MODEL_NAME} --temperature 0.0 --top_p 1.0 --output_file ./outputs/${DEV_SET}/${MODEL_NAME}.jsonl --dev_set ${DEV_SET} --prompt_type gsm8k-demos


DEV_SET=math
CUDA_VISIBLE_DEVICES=${DEVICES} python -m evaluation.inference --model_dir ${ckpts_dir}/${MODEL_NAME} --temperature 0.0 --top_p 1.0 --output_file ./outputs/${DEV_SET}/${MODEL_NAME}.jsonl --dev_set ${DEV_SET} --prompt_type math-demos

# abel_plus: /cpfs01/shared/GAIR/GAIR_hdd/hyzou/math_sft/mistral-7b-sft/abel-plus_lr1e-6_ep3_part
# 