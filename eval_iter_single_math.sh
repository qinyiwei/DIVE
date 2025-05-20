DEVICE=$1
INITSTEP=$2
OUTPUT_DIR=$3
MODEL_NAME=$4
DEV_SET=$5
MODEL_TYPE=$6
PROMPT_TYPE=$7
STEP=$8
MAXSTEP=$9
INSTRUCTION_TYPE=$10

for ckpt in $(seq ${INITSTEP} ${STEP} ${MAXSTEP})
do
    CUDA_VISIBLE_DEVICES=${DEVICE} python -m evaluation.inference \
        --model_dir ${OUTPUT_DIR}/${MODEL_NAME}/checkpoint-${ckpt}  \
        --output_file_name ${OUTPUT_DIR}/${MODEL_NAME}/eval_${ckpt}.jsonl \
        --model_type ${MODEL_TYPE} \
        --temperature 0.0 \
        --top_p 1.0 \
        --dev_set ${DEV_SET} \
        --prompt_type ${PROMPT_TYPE} \
        --answer_key "boxed" \
        --stop "Question" "Answer" \
        --instruction_type ${INSTRUCTION_TYPE}
done