#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
cd $basepath/../../
source env.sh
cd $basepath/../
source setting.conf
cd $basepath

BASE_MODEL=/read-only/common/pretrain_model/transformers/chinese-bert-wwm
VOCAB_PATH=../data/output_vocabulary/
INPUT_FILE=$PREDICT_FILE_DIR/test.txt
OUTPUT_FILE=../../test_data/input.output

# 对输入分词
python segment.py < $INPUT_FILE > ../../test_data/input.tok

# 预测
python predict.py \
    --transformer_model $BASE_MODEL \
    --special_tokens_fix 0 \
    --iteration_count 5 \
    --model_path $SAVE_MODEL_DIR/best.th \
    --vocab_path $VOCAB_PATH \
    --input_file ../../test_data/input.tok \
    --output_file $OUTPUT_FILE \
    --additional_confidence 0. \
    --min_error_probability 0.

# 输出到文件
python convert_result_to_file.py $INPUT_FILE $OUTPUT_FILE > $PREDICT_RESULT_FILE_DIR/predict.txt
