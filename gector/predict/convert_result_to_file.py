import json
import sys

src_path = sys.argv[1]
tgt_path = sys.argv[2]

with open(src_path) as f_src, open(tgt_path) as f_tgt:
    lines_src = f_src.readlines()
    lines_tgt = f_tgt.readlines()
    assert len(lines_src) == len(lines_tgt)
    for i in range(len(lines_src)):
        src_line = lines_src[i].split("\t")[0].strip().replace(" ", "")
        tgt_line = [i.lstrip("##") for i in lines_tgt[i].split(" ") if i.strip() != "[UNK]"]
        tgt_line = "".join(tgt_line).strip()
        if len(tgt_line) == 0:
            tgt_line = "."
        print(src_line.lower().strip() + "\t" + tgt_line.lower().strip())
