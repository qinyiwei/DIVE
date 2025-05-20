#!/bin/bash
MODEL_TYPE="vllm"
PROMPT_TYPE="zero-shot"

DEVICE=$1  # Pass the device number as an argument
MODEL_NAME=$2
DATASET_DIR=$3
SAMPLE_NUM=$4
MODEL_DIR=$5
TEMP=$6
MAX_TOKENS=$7
TRAIN_DATASET_PATH=$8
INSTRUCTION_TYPE=$9

# Calculate the part file number based on DEVICE
if [ "$DEVICE" -ge 4 ]; then
    PART_NUM=$(($DEVICE - 4))
else
    PART_NUM=$DEVICE
fi

PART_FILE="${TRAIN_DATASET_PATH}/part_${PART_NUM}.jsonl"
OUTPUT_FILE="${DATASET_DIR}/${MODEL_NAME}_part${PART_NUM}.jsonl"

# Run the Python command
CUDA_VISIBLE_DEVICES=${DEVICE} python -m evaluation.generation \
    --model_dir ${MODEL_DIR}\
    --output_file_name ${OUTPUT_FILE} \
    --model_type ${MODEL_TYPE} \
    --temperature ${TEMP} \
    --top_p 0.95 \
    --dev_set ${PART_FILE} \
    --prompt_type ${PROMPT_TYPE} \
    --stop "Question" "Answer" \
    --sampling_num ${SAMPLE_NUM} \
    --instruction_type ${INSTRUCTION_TYPE} \
    --max_tokens ${MAX_TOKENS}

