#!/bin/bash

basepath=$(cd `dirname $0`; pwd)
cd $basepath/../../
source env.sh
cd $basepath/../
source setting.conf
cd $basepath

set -e
set -v

BASE_MODEL=/read-only/common/pretrain_model/transformers/chinese-bert-wwm  # 预训练模型文件夹

# 训练样本及输出
TRAIN_FILE_PATH=$TRAIN_FILE_DIR/train.json  # 训练样本文件存放的路径
TRAIN_SOURCE_OUTPUT=../../train_data/train.source  # 分词后的输出文件
TRAIN_TARGET_OUTPUT=../../train_data/train.target  # 分词后的输出文件
TRAIN_FILE=../../train_data/train.data  # 训练序列标注的文件

# 验证样本
VALID_FILE_PATH=.
VALID_SOURCE_OUTPUT=.
VALID_TARGET_OUTPUT=.
VALID_FILE=../../train_data/train.data  # 自己构造验证集

VOCAB_PATH=../data/output_vocabulary/  # 词典
NUM_EPOCH=10
UPDATE_PER_EPOCH=1000

# 构造训练数据，分词
python get_train_data.py --file $TRAIN_FILE_PATH --source_output $TRAIN_SOURCE_OUTPUT --target_output $TRAIN_TARGET_OUTPUT
# 将训练数据转换成标签格式
python ../utils/preprocess_data.py -s $TRAIN_SOURCE_OUTPUT -t $TRAIN_TARGET_OUTPUT -o $TRAIN_FILE

# 构造验证数据，分词
#python get_train_data.py --file $VALID_FILE_PATH --source_output $VALID_SOURCE_OUTPUT --target_output $VALID_TARGET_OUTPUT
# 将验证数据转换成标签格式
#python utils/preprocess_data.py -s $VALID_SOURCE_OUTPUT -t $VALID_TARGET_OUTPUT -o $VALID_FILE

python train.py \
	--train_set $TRAIN_FILE \
	--dev_set $VALID_FILE \
	--model_dir $SAVE_MODEL_DIR \
   --vocab_path $VOCAB_PATH \
	--n_epoch $NUM_EPOCH \
	--cold_steps_count 1 \
	--accumulation_size 2 \
	--updates_per_epoch $UPDATE_PER_EPOCH  \
	--tn_prob 0 \
	--tp_prob 1 \
	--transformer_model $BASE_MODEL \
	--special_tokens_fix 0 \
	--batch_size 32 \
	--pretrain_folder $BASE_MODEL \
	--patience 10 \
