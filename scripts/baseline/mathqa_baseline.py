import sys
sys.path.append('./../')
sys.path.append('./../evaluate_mathqa')

import argparse
import os
from tqdm import tqdm

from scripts.common import read_src_data


def create_pairs(data_points_lst, args):
    src = list()
    tgt = list()
    for item in tqdm(data_points_lst):
        new_src = item['Problem']
        new_tgt = item['linear_formula'].replace(')|', ' ').replace('(', ' ').replace(',', ' '). \
            replace(')', ' ').strip()
        src.append(new_src)
        tgt.append(new_tgt)
    return src, tgt


def write_data(src, tgt, args):
    if not os.path.exists(args.tgt_data_root_dir):
        os.mkdir(args.tgt_data_root_dir)
    file_src = os.path.join(args.tgt_data_root_dir, args.prefix + '_' + 'src.txt')
    print(file_src)
    with open(file_src, 'w') as f:
        for line in src:
            f.write("%s\n" % line)
    file_tgt = os.path.join(args.tgt_data_root_dir, args.prefix + '_' + 'tgt.txt')
    print(file_tgt)
    with open(file_tgt, 'w') as f:
        for line in tgt:
            f.write("%s\n" % line)


def main(args):
    print('## Reading data ##')
    data_points_lst = read_src_data(os.path.join(args.src_data_root_dir, args.src_json))
    print('## Processing data ##')
    src, tgt = create_pairs(data_points_lst, args)
    print('## Writing data ##')
    write_data(src, tgt, args)
    print('## Completed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create a data for base line calculations')
    parser.add_argument('src_data_root_dir', type=str, help='root directory of src data [./../../data/MathQA/MathQAClean]')
    parser.add_argument('src_json', type=str, help='name of the json file. [clean_test.json / clean_train.json / clean_dev.json]')
    parser.add_argument('tgt_data_root_dir', type=str, help='name of the json file. [./../../data/MathQA/MathQABase]')
    parser.add_argument('prefix', type=str, help='prefix used to store the generated files [test_base / train_base / dev_base]')
    args = parser.parse_args()
    main(args)