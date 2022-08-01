#!/usr/bin/env python
# encoding:utf-8
# -------------------------------------------#
# Filename:
#
# Description:
# Version:       1.0
# Company:       www.10jqka.com.cn
#
# -------------------------------------------#
import json
from pathlib import Path
import os
import Levenshtein
from string import punctuation as en_pun
from zhon.hanzi import punctuation as zh_pun

def remove_pun(text):
    _text = ''
    for uchar in text:
        if uchar in en_pun+zh_pun+' 　':
            continue
        _text += uchar
    return _text

def read_input_file(input_file):
    pid_to_text = {}
    with open(input_file, 'r') as f:
        for id, line in enumerate(f):
            line = line.strip().split('\t')
            line = [remove_pun(item.strip()) for item in line]
            pid = str(id)
            text = line[0]
            pid_to_text[pid] = text
    return pid_to_text


def read_label_file(pid_to_text, label_file_list):
    '''
    读取纠正结果
    :param filename:
    :return:
    '''
    error_set, det_set, cor_set = set(), set(), set()
    for line in label_file_list:
        terms = line.strip().split(',')
        terms = [t.strip() for t in terms]
        pid = terms[0]
        if pid not in pid_to_text:
            continue
        if len(terms) == 2 and terms[-1] == '-1':
            continue
        text = pid_to_text[pid]
        if (len(terms)-2) % 4 == 0:
            error_num = int((len(terms)-2) / 4)
            for i in range(error_num):
                loc, typ, wrong, correct = terms[i*4+1: (i+1)*4+1]
                loc = int(loc)
                cor_text = text[:loc] + correct + text[loc+len(wrong):]
                error_set.add((pid, loc, wrong, cor_text))
                det_set.add((pid, loc, wrong))
                cor_set.add((pid, cor_text))
        else:
            raise Exception('check your data format: {}'.format(line))
    # assert len(error_set) == len(det_set) == len(cor_set)
    return error_set, det_set, cor_set


def cal_f1(ref_num, pred_num, right_num):
    precision = float(right_num) / (pred_num + 0.0001)
    recall = float(right_num) / (ref_num + 0.0001)
    if precision + recall < 1e-6:
        return 0.0
    f1 = 2 * precision * recall / (precision + recall + 0.0001)
    return f1 * 100


def evaluate(input_file, ref_file_list, pred_file_list):
    pid_to_text = read_input_file(input_file)
    ref_error_set, ref_det_set, ref_cor_set = read_label_file(pid_to_text, ref_file_list)
    pred_error_set, pred_det_set, pred_cor_set = read_label_file(pid_to_text, pred_file_list)

    ref_num = len(ref_cor_set)
    pred_num = len(pred_cor_set)

    det_right_num = 0
    for error in ref_error_set:
        pid, loc, wrong, cor_text = error
        if (pid, loc, wrong) in pred_det_set or (pid, cor_text) in pred_cor_set:
            det_right_num += 1
    detect_f1 = cal_f1(ref_num, pred_num, det_right_num)
    
    cor_right_num = len(ref_cor_set & pred_cor_set)
    correct_f1 = cal_f1(ref_num, pred_num, cor_right_num)

    final_score = 0.8 * detect_f1 + 0.2 * correct_f1
    return detect_f1, correct_f1, final_score

def convert_from_sentpair2edits(lines_sid, lines_src, lines_tgt):
    assert len(lines_src) == len(lines_tgt) == len(lines_sid)
    convert_result = []
    for i in range(len(lines_src)):
        src_line = lines_src[i].strip()
        tgt_line = lines_tgt[i].strip()
        sid = lines_sid[i].strip()
        edits = Levenshtein.opcodes(src_line, tgt_line)
        result = []
        for edit in edits:
            if "。" in tgt_line[edit[3]:edit[4]]:
                continue
            if edit[0] == "insert":
                result.append((str(edit[1]), "缺失", "", tgt_line[edit[3]:edit[4]]))
            elif edit[0] == "replace":
                result.append((str(edit[1]), "别字", src_line[edit[1]:edit[2]], tgt_line[edit[3]:edit[4]]))
            elif edit[0] == "delete":
                result.append((str(edit[1]), "冗余", src_line[edit[1]:edit[2]], ""))

        out_line = ""
        for res in result:
            out_line +=  ', '.join(res) + ', '
        if out_line:
            convert_result.append(sid + ', ' + out_line.strip())
        else:
            convert_result.append(sid + ', -1')
    return convert_result

class EvalImpl():
    def do_eval(
        self,
        predict_file_dir: Path,
        groundtruth_file_dir: Path,
        result_json_file: Path,
        result_detail_file: Path,
        hparams_path: Path,
        *args,
        **kargs
        
    ):
        """评测主函数

        Args:
            predict_file_dir (Path): input, 模型预测结果的文件目录
            groundtruth_file_dir (Path): input, 真实结果的文件目录
            result_json_file (Path): output, 评测结果，json格式，{"f1": 0.99}
            result_detail_file (Path): output, 预测明细，可选
        """
        print("Eval begin!!")

        pred_map = {}
        pred_id, pred_src, pred_prd = [], [], []
        with open(predict_file_dir) as f:
            for idx, line in enumerate(f):
                line = line.lower().split('\t')
                if len(line) != 2:
                    raise ValueError('line {} length must be 2 after split by \\t, line: {}'.format(idx, line))
                pred_id.append(str(idx))
                pred_src.append(remove_pun(line[0].strip()))
                pred_prd.append(remove_pun(line[1].strip()))
        pred_convert_result = convert_from_sentpair2edits(pred_id, pred_src, pred_prd)
        print(pred_convert_result)
        ref_id, ref_src, ref_prd = [], [], []
        with open(groundtruth_file_dir) as f:
            for idx, line in enumerate(f):
                line = line.lower().split('\t')
                ref_id.append(str(idx))
                ref_src.append(remove_pun(line[0].strip()))
                ref_prd.append(remove_pun(line[1].strip()))
        ref_convert_result = convert_from_sentpair2edits(ref_id, ref_src, ref_prd)
        print(ref_convert_result)
        detect_f1, correct_f1, final_score = evaluate(groundtruth_file_dir, ref_convert_result, pred_convert_result)
        
        result = {"detect": detect_f1, "correct": correct_f1, "score": final_score}
        print(result)
        with open(result_json_file, "w", encoding="utf-8") as fout:
            fout.write(json.dumps(result))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--predict_file_dir", type=str, default="../../groundtruth/")
    parser.add_argument("--groundtruth_file_dir", type=str, default="../../groundtruth/")
    parser.add_argument("--result_json_file", type=str, default="../../output/")
    parser.add_argument("--result_detail_file")
    parser.add_argument("--hparams", default="{}",
                        help="JSON dict of model hyperparameters.")
    args = parser.parse_args()
    eval_object = EvalImpl()
    print(args.predict_file_dir, args.groundtruth_file_dir, args.result_json_file)
    eval_object.do_eval(args.predict_file_dir, args.groundtruth_file_dir, args.result_json_file, args.result_detail_file, args.hparams)
    # python eval.py --predict_file_dir ./output_dir --groundtruth_file_dir ./output_dir --result_json_file output_dir