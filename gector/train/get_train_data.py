import json
import sys
import tokenization
from tqdm import tqdm
import argparse

# 使用平行数据，构造训练集


def read_json(file):
	with open(file, 'r') as fp:
		return [json.loads(l) for l in fp.read().splitlines()]

def write_json(data, file):
	with open(file, 'w') as fp:
		fp.write('\n'.join([json.dumps(l, ensure_ascii=False) for l in data]))

def write_line(data, file):
	with open(file, 'w') as fp:
		fp.write('\n'.join(data))

def preprocess(file, source_file, target_file):
	# 将平行数据，转换成train.src, train.tgt
	data = read_json(file)
	source = [tokenizer_line(l['source']) for l in data]
	target = [tokenizer_line(l['target']) for l in data]
	write_line(source, source_file)
	write_line(target, target_file)


def tokenizer_line(line):
	# 使用分词器，将数据分词
	tokenizer = tokenization.FullTokenizer(vocab_file="vocab.txt", do_lower_case=True)
	line = tokenization.convert_to_unicode(line)
	tokens = tokenizer.tokenize(line)
	return ' '.join(tokens)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file',
                        help='Path to the source file',
                        required=True)
	parser.add_argument('-s', '--source_output',
						help='Path to the source file',
						required=True)
	parser.add_argument('-t', '--target_output',
						help='Path to the source file',
						required=True)
	args = parser.parse_args()
	preprocess(args.file, args.source_output, args.target_output)



