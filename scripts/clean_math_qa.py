import sys
sys.path.append('./evaluate_mathqa')

import argparse
import json
from tqdm import tqdm
import os


from common import  parse_options, execute_prediction


def parse_data_points(data_points_lst):
    correct_formula_count = 0
    options_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    clean_data_points = []
    errored_data_points = []

    for datapoint in tqdm(data_points_lst):
        tgt_formula = datapoint['linear_formula'].replace(')|', ' ').replace('(', ' ').replace(',',' ').\
            replace(')', ' ').strip()
        options = parse_options(datapoint['options'])
        res = execute_prediction(datapoint['Problem'], tgt_formula)
        if res in options:
            if res == options[options_map[datapoint['correct']]]:
                correct_formula_count += 1
                clean_data_points.append(datapoint)
            else:
                errored_data_points.append(datapoint)
        else:
            errored_data_points.append(datapoint)
    return clean_data_points, errored_data_points


def read_src_data(file):
    with open(file) as f:
        data_points_lst = json.load(f)
    return data_points_lst


def convert_nmt_format(data_points):
    src_lst = list()
    tgt_lst = list()
    for item in data_points:
        src_lst.append(item['Problem'])
        tgt_lst.append(item['linear_formula'].replace(')|', ' ').replace('(', ' ').replace(',',' ').
                       replace(')', ' ').strip())

    return src_lst, tgt_lst


def write_data(data_points, prefix, args):
    if not os.path.exists(args.tgt_data_root_dir):
        os.mkdir(args.tgt_data_root_dir)
    json_write_file = os.path.join(args.tgt_data_root_dir, prefix + args.src_json)
    with open(json_write_file, 'w') as f:
        f.write(json.dumps(data_points, indent=1))
    src_lst, tgt_lst = convert_nmt_format(data_points)
    src_file = os.path.join(args.tgt_data_root_dir, prefix + args.src_json + '_src.txt')
    tgt_file = os.path.join(args.tgt_data_root_dir, prefix + args.src_json + '_tgt.txt')
    with open(src_file, 'w') as f:
        for line in src_lst:
            f.write("%s\n" % line)
    with open(tgt_file, 'w') as f:
        for line in src_lst:
            f.write("%s\n" % line)


def main(args):
    print('## Reading data ##')
    data_points_lst = read_src_data(os.path.join(args.src_data_root_dir, args.src_json))
    print('## Validating / Extracting correct data points ##')
    clean_data_points, errored_data_points = parse_data_points(data_points_lst)
    print('## Writing data ##')
    write_data(clean_data_points, 'clean_', args)
    write_data(errored_data_points, 'error_', args)
    print('Length of clean data ', len(clean_data_points))
    print('Length of errored data ', len(errored_data_points))
    print('## Completed ##')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='clean up the math qa dataset')
    parser.add_argument('src_data_root_dir', type=str, help='root directory of src data [./../data/MathQA]')
    parser.add_argument('src_json', type=str, help='name of the json file. [test.json / train.json / dev.json]')
    parser.add_argument('tgt_data_root_dir', type=str, help='name of the json file. [./../data/MathQA/MathQAClean]')
    args = parser.parse_args()
    main(args)
