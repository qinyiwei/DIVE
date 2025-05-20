export WANDB_MODE=disabled

#Training Hyper parameters
BETA=4e-1
FTX_GAMMA=5e-1
LOSS_TYPE="sigmoid"
LR=3e-8
LR_SCHEDULER="constant"
TRAIN_SETTING="lr${LR}-${LR_SCHEDULER}-beta${BETA}-ftx_gamma_${FTX_GAMMA}-epoch-loss-${LOSS_TYPE}"

#Sample Setting
TEMP=0.7
SAMPLE_NUM=8
MAX_TOKENS=1024
FIX_PAIR=2
SAMPLE_SETTING="SAMPLE_${SAMPLE_NUM}_TEMP_${TEMP}_MAX_TOKENS_${MAX_TOKENS}"
PREFERENCE_SETTING="num_pair_${FIX_PAIR}"


SFT_MODEL="/nas/shared/GAIR/ckpts/mistralai/Mistral-7B-v0.1/"
TEST_DATASET="data/toy_example/math_sub.jsonl"
TRAIN_DATASET_PATH="data/toy_example/"
DATASET_DIR_ROOT="iterative_dpo_data/MATH/initial_model_mistral-7b-sft"
INSTRUCTION_TYPE="sft"
ANSWER_KEY="boxed"
OUTPUT_DIR="iterative_dpo_model/MATH/initial_model_mistral-7b-sft/${SAMPLE_SETTING}/${PREFERENCE_SETTING}/${TRAIN_SETTING}"

#Host Setting
HOSTS=(0 1 2 3)
HOSTS_STRING="localhost:${HOSTS[0]}"
for i in "${HOSTS[@]:1}"; do
    HOSTS_STRING+=",${i}"
done
DEVICE=${HOSTS[0]}
GPU_LIST="${HOSTS[0]}"
for i in "${HOSTS[@]:1}"; do
    GPU_LIST+=",${i}"
done

#Iterative Setting
ITERS=(1)



# Check if DATASET_DIR_ROOT does not exist
if [ ! -d "$DATASET_DIR_ROOT" ]; then
    echo "dataset directory ${DATASET_DIR_ROOT} does not exist, create it"
    # Create DATASET_DIR_ROOT
    mkdir -p "$DATASET_DIR_ROOT"
fi


DATASET_DIR_SAMPLE="${DATASET_DIR_ROOT}/${SAMPLE_SETTING}"

# Check if DATASET_DIR_SAMPLE does not exist
if [ ! -d "$DATASET_DIR_SAMPLE" ]; then
    echo "dataset directory ${DATASET_DIR_SAMPLE} does not exist, create it"
    # Create DATASET_DIR_SAMPLE
    mkdir -p "$DATASET_DIR_SAMPLE"
fi

if [ ! -f "$DATASET_DIR_SAMPLE/M0-samples.jsonl" ] || [ ! -s "$DATASET_DIR_SAMPLE/M0-samples.jsonl" ]; then
    MODEL_NAME="mistral-7b-sft"
    echo "-------------------${MODEL_NAME}(M0): Generate Samples---------------------"
    echo "DATASET_DIR_SAMPLE=${DATASET_DIR_SAMPLE}"
    for i in "${HOSTS[@]}"; do
        nohup bash generate_preference_data.sh $i $MODEL_NAME $DATASET_DIR_SAMPLE $SAMPLE_NUM $SFT_MODEL $TEMP $MAX_TOKENS $TRAIN_DATASET_PATH $INSTRUCTION_TYPE\
            > ${DATASET_DIR_SAMPLE}/generate_preference_data_${MODEL_NAME}_gpu${i}.log 2>&1 &
    done
    wait


    echo "---------------------${MODEL_NAME}(M0): Merge part sample files---------------------"
    for i in "${HOSTS[@]}"; do
        # Calculate the part file number based on DEVICE
        if [ "$i" -ge 4 ]; then
            PART_NUM=$(($i - 4))
        else
            PART_NUM=$i
        fi
        cat $DATASET_DIR_SAMPLE/${MODEL_NAME}_part${PART_NUM}.jsonl >> ${DATASET_DIR_SAMPLE}/M0-samples.jsonl
    done
fi

if [ ! -f "$DATASET_DIR_SAMPLE/dataset_info.json" ]; then
    echo "---------------------${MODEL_NAME}(M0): create dataset_info.json file---------------------"
    # Define ITER and the JSON file path
    DATASET_INFO_FILE=${DATASET_DIR_SAMPLE}/dataset_info.json

    # Check if the JSON file exists, create it with an empty object if it does not
    if [ ! -f "$DATASET_INFO_FILE" ]; then
        echo "Creating new JSON file: $DATASET_INFO_FILE with an empty object."
        echo "{}" > "$DATASET_INFO_FILE"
    fi

    # Generate the key and file_name based on ITER
    KEY="M0"
    FILE_NAME="${KEY}-samples_preference.jsonl"

    # Check if the key already exists
    if jq -e '.["'"$KEY"'"]' $DATASET_INFO_FILE > /dev/null; then
        echo "Key $KEY already exists in $DATASET_INFO_FILE."
    else
        # Add new key-value pair to JSON file
        jq '. + {"'"$KEY"'": {"file_name": "'"$FILE_NAME"'", "columns": {"prompt": "instruction", "response": "output"}}}' $DATASET_INFO_FILE > temp.json && mv temp.json $DATASET_INFO_FILE
        echo "Added $KEY to $DATASET_INFO_FILE."
    fi    
fi




DATASET_DIR_INIT="${DATASET_DIR_SAMPLE}/${PREFERENCE_SETTING}"
DATASET_DIR_ITERS="${DATASET_DIR_SAMPLE}/${PREFERENCE_SETTING}/${TRAIN_SETTING}"

# Check if DATASET_DIR_INIT does not exist
echo $DATASET_DIR_INIT
if [ ! -d "$DATASET_DIR_INIT" ]; then
    echo "dataset directory ${DATASET_DIR_INIT} does not exist, create it"
    # Create DATASET_DIR_INIT
    mkdir -p "$DATASET_DIR_INIT"

    # Copy dataset_info.json to DATASET_DIR_INIT
    cp "${DATASET_DIR_SAMPLE}/dataset_info.json" "$DATASET_DIR_INIT"

    # Copy M0-samples.jsonl to DATASET_DIR_INIT
    cp "${DATASET_DIR_SAMPLE}/M0-samples.jsonl" "$DATASET_DIR_INIT"
fi

if [ ! -f "$DATASET_DIR_INIT/M0-samples_preference.jsonl" ]; then
    echo "-------------------M0: Construct Preference Data---------------------"
    python get_preference_data.py \
        --pred_file "${DATASET_DIR_INIT}/M0-samples.jsonl" \
        --output_file_append "preference" \
        --fix_pair ${FIX_PAIR} \
        --answer_key ${ANSWER_KEY}
fi

for ITER in "${ITERS[@]}"
do
    DATASET="M$((ITER - 1))"
    MODEL_NAME="M${ITER}"
    OUTPUT_MODEL_DIR="${OUTPUT_DIR}/${MODEL_NAME}"
    if [ $ITER -eq 1 ]; then
        DATASET_DIR=$DATASET_DIR_INIT
    else
        DATASET_DIR=$DATASET_DIR_ITERS
    fi


    echo "---------------------${MODEL_NAME}: Get BASE model of current ITER---------------------"
    if [ $ITER -eq 1 ]; then
        MODEL_NAME_OR_PATH=$SFT_MODEL
    else
        MODEL_NAME_OR_PATH="${OUTPUT_DIR}/M$((ITER - 1))"
    fi


    echo "-------------------${MODEL_NAME}: Training---------------------"
    echo ${HOSTS_STRING}
    deepspeed --include ${HOSTS_STRING} --master_port 11304 LLaMA-Factory/src/train_bash.py \
        --deepspeed LLaMA-Factory/examples/full_multi_gpu/ds_z3_config.json \
        --stage dpo \
        --do_train \
        --model_name_or_path ${MODEL_NAME_OR_PATH} \
        --ref_model ${MODEL_NAME_OR_PATH} \
        --dataset ${DATASET} \
        --dataset_dir ${DATASET_DIR} \
        --template default \
        --finetuning_type full \
        --output_dir ${OUTPUT_MODEL_DIR} \
        --overwrite_cache \
        --overwrite_output_dir \
        --per_device_train_batch_size 8 \
        --gradient_accumulation_steps 2 \
        --lr_scheduler_type ${LR_SCHEDULER} \
        --logging_steps 10 \
        --learning_rate ${LR} \
        --plot_loss \
        --fp16 \
        --num_train_epochs 1 \
        --dpo_beta ${BETA} \
        --dpo_loss ${LOSS_TYPE} \
        --dpo_ftx ${FTX_GAMMA} \
        --keep_attributes "num_crt,num_wrg"

 

    echo "-------------------${MODEL_NAME}: Evaluation---------------------"
    MODEL_TYPE="vllm"
    PROMPT_TYPE="zero-shot" # ["zero-shot" "few-shot"]

    CUDA_VISIBLE_DEVICES=${DEVICE} python -m evaluation.inference \
            --model_dir ${OUTPUT_DIR}/${MODEL_NAME}  \
            --output_file_name ${OUTPUT_DIR}/${MODEL_NAME}/eval_epoch.jsonl \
            --model_type ${MODEL_TYPE} \
            --temperature 0.0 \
            --top_p 1.0 \
            --dev_set ${TEST_DATASET} \
            --prompt_type ${PROMPT_TYPE} \
            --answer_key ${ANSWER_KEY} \
            --stop "Question" "Answer" \
            --instruction_type $INSTRUCTION_TYPE
    

    echo "-------------------${MODEL_NAME}: Generate Samples---------------------"
    echo "DATASET_DIR_ITERS=${DATASET_DIR_ITERS}"
    # Check if the directory exists, and create it if it does not
    if [ ! -d "$DATASET_DIR_ITERS" ]; then
        echo "Creating directory $DATASET_DIR_ITERS"
        mkdir -p "$DATASET_DIR_ITERS"
    else
        echo "Directory $DATASET_DIR_ITERS already exists."
    fi


    for i in "${HOSTS[@]}"; do
        nohup bash generate_preference_data.sh $i $MODEL_NAME $DATASET_DIR_ITERS $SAMPLE_NUM $OUTPUT_MODEL_DIR $TEMP $MAX_TOKENS $TRAIN_DATASET_PATH $INSTRUCTION_TYPE\
            > ${DATASET_DIR_ITERS}/generate_preference_data_${MODEL_NAME}_gpu${i}.log 2>&1 &
    done
    wait

    echo "---------------------${MODEL_NAME}: Merge part sample files---------------------"
    for i in "${HOSTS[@]}"; do
        # Calculate the part file number based on DEVICE
        if [ "$i" -ge 4 ]; then
            PART_NUM=$(($i - 4))
        else
            PART_NUM=$i
        fi
        cat $DATASET_DIR_ITERS/${MODEL_NAME}_part${PART_NUM}.jsonl >> ${DATASET_DIR_ITERS}/${MODEL_NAME}-samples.jsonl
    done



    echo "-------------------${MODEL_NAME}: Construct Preference Data---------------------"
    python get_preference_data.py \
        --pred_file "${DATASET_DIR_ITERS}/${MODEL_NAME}-samples.jsonl" \
        --output_file_append "preference" \
        --fix_pair ${FIX_PAIR} \
        --answer_key ${ANSWER_KEY}


    echo "---------------------${MODEL_NAME}: Add new preference data info to the dataset_info.json file---------------------"
    # Define ITER and the JSON file path
    DATASET_INFO_FILE=${DATASET_DIR_ITERS}/dataset_info.json

    # Check if the JSON file exists, create it with an empty object if it does not
    if [ ! -f "$DATASET_INFO_FILE" ]; then
        echo "Creating new JSON file: $DATASET_INFO_FILE with an empty object."
        echo "{}" > "$DATASET_INFO_FILE"
    fi

    # Generate the key and file_name based on ITER
    KEY="M${ITER}"
    FILE_NAME="${KEY}-samples_preference.jsonl"

    # Check if the key already exists
    if jq -e '.["'"$KEY"'"]' $DATASET_INFO_FILE > /dev/null; then
        echo "Key $KEY already exists in $DATASET_INFO_FILE."
    else
        # Add new key-value pair to JSON file
        jq '. + {"'"$KEY"'": {"file_name": "'"$FILE_NAME"'", "columns": {"prompt": "instruction", "response": "output"}}}' $DATASET_INFO_FILE > temp.json && mv temp.json $DATASET_INFO_FILE
        echo "Added $KEY to $DATASET_INFO_FILE."
    fi    
done