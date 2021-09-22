import sys
sys.path.append('../evaluate_mathqa')

import argparse
from multiprocessing import Pool
import json
from scripts.common import execute_prediction, parse_options
from tqdm import tqdm

src_json = dict()


def read_src_json(file):
    global src_json
    with open(file) as f:
        src_data_points_lst = json.load(f)
    for item in src_data_points_lst:
        src_json[item['Problem'].strip()] = item


def read_file(file):
    with open(file) as f:
        lines = f.readlines()
    return lines


def evaluate(src, tgt):
    key = src.split('[SEP]')[0]
    key = key.strip()
    res = execute_prediction(key, tgt)
    options = parse_options(src_json[key]['options'])
    options_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    if res in options:
        if res == options[options_map[src_json[key]['correct']]]:
            return 1
        else:
            return 0
    else:
        return 0


def process_preds(pb_pred_zip):
    for tgt in pb_pred_zip[1]:
        if evaluate(pb_pred_zip[0], tgt):
            return 1
    return 0


def main(args):
    pbs = read_file(args.src_pb)
    pred = read_file(args.pred)
    n_bst = args.n_best
    pb_pred_zip = [(pbs[i], pred[i * n_bst: i * n_bst + n_bst]) for i in range(len(pbs))]
    print('## Evaluating ..')
    with Pool(processes=10, initializer=read_src_json, initargs=[args.src_data_json]) as p:
        ret = p.map(process_preds, pb_pred_zip)
        valid = sum(ret)
    # for i, src in tqdm(enumerate(pbs)):
    #     for tgt in pred[i*n_bst: i*n_bst+n_bst]:
    #         if evaluate(src, tgt):
    #             valid = valid + 1
    #             break

    print('## Number correctly predicted ##', valid)
    print('## Number in-correctly predicted ##', len(pbs) - valid)
    print('## Accuracy ##', valid / len(pbs))
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate on the test set')
    parser.add_argument('src_data_json', type=str, help='Root directory of src json [./../data/MathQA/MathQAClean/clean_test.json]')
    parser.add_argument('src_pb', type=str, help='Source data contianing problems in format "<PROBLEM> [SEP] <SYMBOLIC INSTRUCTION>"')
    parser.add_argument('pred', type=str, help='Predictions for the source file containing symbolic instructions')
    parser.add_argument('n_best', type=int, help='Total number of predictions per question')
    args = parser.parse_args()
    main(args)
