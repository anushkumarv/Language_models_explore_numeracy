import argparse
import json
import os
import re

ANS_TOKEN = "\\boxed"
EXCEPTION_DIR = ['']


def main(args):
    data_points_list = list()
    root = args.dataset_root
    pb_dirs = fetch_pb_dirs(root)
    for dir in pb_dirs:
        if dir not in EXCEPTION_DIR:
            files = [item for item in os.listdir(os.path.join(root, dir)) if 'json' in item]
            for file in files:
                try:
                    data_points_list.append(fetch_datapoint(os.path.join(root, dir, file)))
                except Exception as e:
                    continue
            write_ops(args, dir, data_points_list)


def write_ops(args, dir_name, data_points_list):
    src_file_name = os.path.join(args.dataset_root, dir_name + '_src.txt')
    tgt_file_name = os.path.join(args.dataset_root, dir_name + '_tgt.txt')
    with open(src_file_name, 'w') as src_f, open(tgt_file_name, 'w') as tgt_f:
        for item in data_points_list:
            src_f.write(item[0].strip().replace("\n", "") + '\n')
            tgt_f.write(str(item[1]) + '\n')


def fetch_pb_dirs(root):
    return [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]


def fetch_datapoint(file_path):
    with open(file_path) as f:
        datapoint = json.load(f)
    return datapoint['problem'], fetch_answer(datapoint['solution'])


def fetch_answer(solution):
    for token in solution.split()[::-1]:
        if ANS_TOKEN in token:
            return parse_answer(token)
    raise Exception


def parse_answer(token):
    box_ans = re.search('boxed{(.*)}', token).group(1)
    try:
        req_ans = int(box_ans)
        return req_ans
    except Exception as e:
        frac_ans = re.search('frac{(.*)}{(.*)}', box_ans)
        if frac_ans:
            return int(frac_ans.group(1)) / int(frac_ans.group(2))
        dfrac_ans = re.search('dfrac{(.*)}{(.*)}', box_ans)
        if dfrac_ans:
            return int(dfrac_ans.group(1)) / int(dfrac_ans.group(2))
        raise Exception


parser = argparse.ArgumentParser(description='parse math data')
parser.add_argument('dataset_root', type=str, help='path pointing to train/test dir')
args = parser.parse_args()
main(args)
